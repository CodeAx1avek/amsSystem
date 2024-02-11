from django.urls import path
from django.contrib import admin
from .views import home,dashboard,login_view

urlpatterns = [
    path("",home,name="home"),
    path('login/',login_view, name='login'),
    path('dashboard/',dashboard, name='dashboard'),
]
