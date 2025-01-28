from django.urls import path

from cost_tracker.main.views import *

urlpatterns = (

    path('', main_dashboard, name='main-dashboard'),
    # path('wat_usa/', include([
    #     path('why_usa/', why_usa_tab, name='why usa'),
    #     path('who/', who_tab, name='who'),
    #     path('how/', how_tab, name='how'),
    #     path('price/', price_tab, name='price'),
    #     path('needed_docs', needed_docs, name='needed documents'),
    # ])),

)
