from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticketmaster, name="ticketmaster"),
    path('event/view/<str:event_id>', views.view_event, name='view_event'),
    # path('', views.get_event_search, name="get-event-search")

]
