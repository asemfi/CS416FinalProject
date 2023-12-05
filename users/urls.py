from django.urls import path
from . import views


urlpatterns =[
    path('', views.view_users, name='view_users'),
    path('add', views.add_product, name='add'),
    path('update', views.update_product, name='update'),
    path('delete', views.delete_product, name='delete')

]
