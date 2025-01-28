from django.contrib import admin
from django.db.models import Sum

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'category', 'comment')  # Fields to display
    list_filter = ('user', 'category', 'date', 'comment')  # Filters
    search_fields = ('user__username', 'category', 'comment')  # Search bar
    ordering = ('-date',)  # Default ordering

    def changelist_view(self, request, extra_context=None):
        # Handle POST requests separately (e.g., saving/deleting actions)
        if request.method == "POST":
            return super().changelist_view(request, extra_context=extra_context)

        # Handle GET requests for displaying the changelist
        response = super().changelist_view(request, extra_context=extra_context)

        # Only proceed if the response has a context (i.e., it's not a redirect)
        if hasattr(response, 'context_data'):
            try:
                # Access the filtered queryset
                cl = response.context_data["cl"]
                queryset = cl.queryset

                # Calculate totals based on the filtered queryset
                total_amount = queryset.aggregate(Sum('amount'))['amount__sum'] or 0
            except (AttributeError, KeyError):
                # Default total if queryset is unavailable
                total_amount = 0

            # Add the total to the context
            extra_context = extra_context or {}
            extra_context['total_amount'] = total_amount

            # Update the response context with totals
            response.context_data.update(extra_context)

        return response


admin.site.register(Expense, ExpenseAdmin)
