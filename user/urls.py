from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import login

app_name = 'user'
urlpatterns = [
    path('login', login, {'template_name': 'user/login.html'}, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
]
