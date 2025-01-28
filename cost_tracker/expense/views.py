from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Func, Count, F, Value
from django.db.models.functions import TruncMonth
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic as views

from cost_tracker.expense.forms import AddExpenseForm, ExcelUploadForm
from cost_tracker.expense.models import Expense

User = get_user_model()


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH FROM %(expressions)s)'


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR FROM %(expressions)s)'


class AddExpense(views.CreateView):
    model = Expense
    form_class = AddExpenseForm
    template_name = 'add-expense.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def get_success_url(self):
        return reverse_lazy('list-expense', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user  # Set the user field to the logged-in user
        return super().form_valid(form)


class ExpenseEntryListView(LoginRequiredMixin, views.ListView):
    model = Expense
    template_name = 'list-expense.html'
    context_object_name = 'expense_list'
    ordering = ['id']

    def get_queryset(self):
        user_pk = self.request.user
        return Expense.objects.filter(user=user_pk).order_by('-id')


class EditExpenseView(LoginRequiredMixin, views.UpdateView):
    model = Expense
    form_class = AddExpenseForm
    template_name = 'edit_expense.html'
    context_object_name = 'edit_expense'

    def get_object(self, queryset=None):
        # Fetch the tax object by primary key
        expense = get_object_or_404(Expense, pk=self.kwargs['pk'])

        # Check if the tax object's user matches the current user
        if expense.user != self.request.user:
            return HttpResponseForbidden("You do not have permission to edit this tax form.")

        # If they match, return the tax object
        return expense

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_tax'] = get_object_or_404(Taxes, user=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Ensure the user field remains consistent
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-expense', kwargs={'pk': self.request.user.pk})


# class ExpenseDetailView(views.ListView):
#     model = Expense
#     template_name = 'expense_detail.html'
#     context_object_name = 'expenses'
#
#     def get_queryset(self):
#         """
#         Fetches and filters the queryset based on user and optional filters.
#         """
#         user = self.request.user
#         month = self.request.GET.get('month', None)
#         year = self.request.GET.get('year', None)
#         category = self.request.GET.get('category', None)
#         comment = self.request.GET.get('comment', None)
#
#         # Base queryset for the current user
#         queryset = Expense.objects.filter(user=user)
#
#         # Apply filters
#         if year:
#             queryset = queryset.filter(date__year=year)
#         if month:
#             queryset = queryset.filter(date__month=month)
#         if category:
#             queryset = queryset.filter(category=category)
#         if comment:
#             queryset = queryset.filter(comment__icontains=comment)
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         """
#         Adds additional context for rendering the template.
#         """
#         context = super().get_context_data(**kwargs)
#
#         # Current year and month
#         current_year = datetime.now().year
#         current_month = datetime.now().month
#         context['current_year'] = current_year
#         context['current_month'] = current_month
#
#         # Filtering the queryset
#         expenses = self.get_queryset()
#
#         # Aggregations
#         context['total_by_category_month'] = expenses.values('category', 'date__year', 'date__month') \
#             .annotate(total_amount=Sum('amount')) \
#             .order_by('category', 'date__year', 'date__month')
#
#         context['total_by_category_year'] = (
#             expenses.annotate(
#                 month=Month('date'),
#                 year=Year('date')
#             )
#             .values('category', 'date__year')
#             .annotate(
#                 total_amount=Sum('amount'),
#                 unique_months=Count('month', distinct=True),
#                 average_per_month=F('total_amount') / F('unique_months')
#             )
#             .order_by('-total_amount', 'category', 'date__year')
#         )
#
#         # Distinct comments for the dropdown
#         context['distinct_comments'] = expenses.values_list('comment', flat=True).distinct()
#
#         # Categories for dropdown
#         context['categories'] = Expense.CATEGORY
#
#         # Year range for the dropdown
#         context['years'] = range(2020, current_year + 1)
#
#         return context

#
class ExpenseDetailView(views.ListView):
    model = Expense
    template_name = 'expense_detail.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Get the filter parameters from the URL
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)
        category = self.request.GET.get('category', None)
        comment = self.request.GET.get('comment', None)

        # Start with filtering by user
        queryset = Expense.objects.filter(user=user).order_by('-date')

        # Filter by month and/or year if provided
        if year and year != "All":
            queryset = queryset.filter(date__year=year)
        if month and month != "All":
            queryset = queryset.filter(date__month=month)

        # Filter by category if provided
        if category and category != "All":
            queryset = queryset.filter(category=category)

        # Filter by comment if provided
        if comment and comment != "All":
            queryset = queryset.filter(comment__icontains=comment)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Current year and month
        current_year = datetime.now().year
        current_month = datetime.now().month
        context['current_year'] = current_year
        context['current_month'] = current_month

        # Get the queryset with applied filters
        expenses = self.get_queryset()

        # Define a function to calculate past months in a year
        def calculate_past_months(year):
            if year == current_year:
                return current_month
            elif year == 2024:
                return 7
            elif year < current_year:
                return 12
            else:
                return 0  # Future years have no past months

        # Get all years present in the filtered expenses
        years_in_data = expenses.annotate(year=Year('date')).values_list('date__year', flat=True).distinct()

        # Create a dictionary to store past months for each year
        past_months_by_year = {year: calculate_past_months(year) for year in years_in_data}

        # Aggregations
        context['total_by_category_month'] = expenses.values('category', 'date__year', 'date__month') \
                .annotate(total_amount=Sum('amount')) \
                .order_by('category', 'date__year', 'date__month')

        context['total_by_category_year'] = (
            expenses.annotate(
                year=Year('date')
            )
            .values('category', 'date__year')
            .annotate(
                total_amount=Sum('amount'),
                average_per_month=F('total_amount') / Value(1)  # Placeholder for division
            )
            .order_by('-total_amount', 'category', 'date__year')
        )

        # Update `average_per_month` by dividing by the number of past months
        for item in context['total_by_category_year']:
            year = item['date__year']
            past_months = past_months_by_year.get(year, 0)
            item['average_per_month'] = item['total_amount'] / past_months if past_months > 0 else 0

        # Distinct comments for the dropdown
        distinct_comments = (
            Expense.objects.filter(user=self.request.user)
            .exclude(comment__isnull=True)  # Exclude None values
            .exclude(comment__exact='')  # Exclude empty strings
            .values_list('comment', flat=True)
            .distinct()
        )
        context['distinct_comments'] = ["All"] + list(distinct_comments)  # Add "All" at the beginning

        # Categories for dropdown
        context['categories'] = Expense.CATEGORY

        # Year range for the dropdown
        context['years'] = range(2020, current_year + 1)

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     # Current year and month
    #     current_year = datetime.now().year
    #     current_month = datetime.now().month
    #     context['current_year'] = current_year
    #     context['current_month'] = current_month
    #
    #     # Get the queryset with applied filters
    #     expenses = self.get_queryset()
    #
    #     total_unique_months = Expense.objects.filter(user=self.request.user) \
    #         .annotate(month=TruncMonth('date')) \
    #         .values('month') \
    #         .distinct() \
    #         .count()
    #
    #     # Aggregations
    #     context['total_by_category_month'] = expenses.values('category', 'date__year', 'date__month') \
    #         .annotate(total_amount=Sum('amount')) \
    #         .order_by('category', 'date__year', 'date__month')
    #
    #     context['total_by_category_year'] = (
    #         expenses.annotate(
    #             month=Month('date'),
    #             year=Year('date')
    #         )
    #         .values('category', 'date__year')
    #         .annotate(
    #             total_amount=Sum('amount'),
    #             unique_months=Count('month', distinct=True),
    #             average_per_month=F('total_amount') / F('unique_months')
    #         )
    #         .order_by('-total_amount', 'category', 'date__year')
    #     )
    #
    #     # Distinct comments for the dropdown
    #     distinct_comments = (
    #         Expense.objects.filter(user=self.request.user)
    #         .exclude(comment__isnull=True)  # Exclude None values
    #         .exclude(comment__exact='')    # Exclude empty strings
    #         .values_list('comment', flat=True)
    #         .distinct()
    #     )
    #     context['distinct_comments'] = ["All"] + list(distinct_comments)  # Add "All" at the beginning
    #
    #     # Categories for dropdown
    #     context['categories'] = Expense.CATEGORY
    #
    #     # Year range for the dropdown
    #     context['years'] = range(2020, current_year + 1)
    #
    #     return context


@login_required
def upload_expenses(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Read the Excel file
                data = pd.read_excel(file)

                # Iterate through the rows and create Expense objects for the logged-in user
                for _, row in data.iterrows():
                    Expense.objects.create(
                        user=request.user,  # Assign the currently logged-in user
                        amount=row.get('Amount'),
                        date=row.get('Date'),
                        category=row.get('Category'),
                        comment=row.get('Comment'),
                    )
                return render(request, 'expense_detail.html')
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}")

    else:
        form = ExcelUploadForm()

    return render(request, 'upload_expenses.html', {'form': form})