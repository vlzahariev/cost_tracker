from django.urls import path

from cost_tracker.income.views import *

urlpatterns = (
    path('add-income/', AddIncome.as_view(), name='add-income'),
    path('list-income/<int:pk>/', IncomeEntryListView.as_view(), name='list-income'),
    path('edit-income/<int:pk>/', EditIncomeView.as_view(), name='edit-income'),

    # path('wat_usa/', include([
    #     path('why_usa/', why_usa_tab, name='why usa'),
    #     path('who/', who_tab, name='who'),
    #     path('how/', how_tab, name='how'),
    #     path('price/', price_tab, name='price'),
    #     path('needed_docs', needed_docs, name='needed documents'),
    # ])),

)
