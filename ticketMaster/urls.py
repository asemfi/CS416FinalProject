from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticketmaster, name="ticketmaster"),
    path('event/view/<str:event_id>', views.view_event, name='view_event'),
    path('event/view/<str:event_id>/update_comment', views.update_comment, name='update_comment'),
    path('event/view/<str:event_id>/delete_comment', views.delete_comment, name='delete_comment'),
    path('event/view/<str:event_id>/create_comment', views.create_comment, name='create_comment'),
]
