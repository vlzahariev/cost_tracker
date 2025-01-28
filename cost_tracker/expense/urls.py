from django.urls import path

from cost_tracker.expense.views import *

urlpatterns = (
    path('add-expense/', AddExpense.as_view(), name='add-expense'),
    path('list-expense/<int:pk>/', ExpenseEntryListView.as_view(), name='list-expense'),
    path('edit-expense/<int:pk>/', EditExpenseView.as_view(), name='edit-expense'),
    path('expenses/', ExpenseDetailView.as_view(), name='expense_detail'),
    path('upload-expenses/', upload_expenses, name='upload_expenses'),

    # path('wat_usa/', include([
    #     path('why_usa/', why_usa_tab, name='why usa'),
    #     path('who/', who_tab, name='who'),
    #     path('how/', how_tab, name='how'),
    #     path('price/', price_tab, name='price'),
    #     path('needed_docs', needed_docs, name='needed documents'),
    # ])),

)
