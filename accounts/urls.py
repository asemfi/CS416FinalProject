from django.contrib import admin
from django.urls import path, include

from ticketMaster import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout")

]
