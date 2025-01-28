from django.contrib.auth import logout, get_user_model
from django.db.models import Sum, Avg, Max
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import make_aware, get_current_timezone
from django.views.generic import UpdateView
from datetime import datetime, timedelta

from cost_tracker.income.models import Income
from cost_tracker.expense.models import Expense


# Create your views here.


import plotly.graph_objects as go
from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Avg


User = get_user_model()


def main_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    # Get the latest date from both Income and Expense
    latest_income_date = Income.objects.filter(user=user).aggregate(Max('date'))['date__max']
    latest_expense_date = Expense.objects.filter(user=user).aggregate(Max('date'))['date__max']

    # Determine the most recent date
    latest_date = max(latest_income_date, latest_expense_date)
    if latest_date is None:
        latest_date = datetime.now().date()  # Default to today's date if no data exists

    # Convert `date` to `datetime` and calculate the start date
    latest_datetime = datetime.combine(latest_date, datetime.min.time())  # Start of the day
    start_datetime = latest_datetime - timedelta(days=365) + timedelta(days=1)  # Inclusive 1-year range

    # Apply timezone awareness
    tz = get_current_timezone()
    latest_datetime = make_aware(latest_datetime, timezone=tz)
    start_datetime = make_aware(start_datetime, timezone=tz)

    # Filter data within the last year
    income_data = Income.objects.filter(user=user, date__range=(start_datetime, latest_datetime)) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total_income=Sum('amount')) \
        .order_by('month')

    expense_data = Expense.objects.filter(user=user, date__range=(start_datetime, latest_datetime)) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(total_expense=Sum('amount')) \
        .order_by('month')

    # Combine income and expense data by month
    combined_data = {}
    for entry in income_data:
        month_str = entry['month'].strftime('%b %Y')
        combined_data[month_str] = {'income': entry['total_income'], 'expense': 0}

    for entry in expense_data:
        month_str = entry['month'].strftime('%b %Y')
        if month_str in combined_data:
            combined_data[month_str]['expense'] = entry['total_expense']
        else:
            combined_data[month_str] = {'income': 0, 'expense': entry['total_expense']}

    # Sort combined data by month
    sorted_combined_data = dict(
        sorted(combined_data.items(), key=lambda x: datetime.strptime(x[0], '%b %Y'))
    )

    # Prepare data for the chart
    months = list(sorted_combined_data.keys())
    income_totals = [entry['income'] for entry in sorted_combined_data.values()]
    expense_totals = [entry['expense'] for entry in sorted_combined_data.values()]

    # Create combined graph
    combined_fig = go.Figure()
    combined_fig.add_trace(go.Bar(x=months, y=income_totals, name='Income', marker_color='lightgreen'))
    combined_fig.add_trace(go.Bar(x=months, y=expense_totals, name='Expense', marker_color='lightcoral'))
    combined_fig.update_layout(
        title=f'Income vs Expense (Last Year from {latest_datetime.strftime("%b %Y")})',
        xaxis=dict(title='Month'),
        yaxis=dict(title='Amount'),
        barmode='group',  # Grouped bars for comparison
        template='plotly_white'
    )
    combined_plot = combined_fig.to_html(full_html=False)

    # Calculate totals and averages
    total_income = sum(income_totals)
    total_expense = sum(expense_totals)
    unique_months = len(months)
    avg_income = total_income / unique_months if unique_months > 0 else 0
    avg_expense = total_expense / unique_months if unique_months > 0 else 0

    # Pass data to the template
    return render(request, 'dashboard.html', {
        'total_income': total_income,
        'avg_income': avg_income,
        'total_expense': total_expense,
        'avg_expense': avg_expense,
        'combined_plot': combined_plot,
    })


def custom_logout_page(request):
    logout(request)
    return redirect('/')


class EditUserView(UpdateView):
    model = User
    template_name = 'edit_user.html'
    fields = ['first_name', 'last_name', 'email']  # Fields to edit
    success_url = reverse_lazy('main-dashboard')  # Redirect to home page after successful update

    def get_object(self, queryset=None):
        # Ensure only the logged-in user can edit their details
        return self.request.user
