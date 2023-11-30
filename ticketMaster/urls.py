from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticketmaster, name="ticketmaster"),
    # path('', views.get_event_search, name="get-event-search")

]
