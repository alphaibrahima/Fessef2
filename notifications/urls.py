from django.contrib import admin
from django.urls import path, include
from notifications.views import  ShowNotifications


urlpatterns = [
    path('', ShowNotifications, name='notifications'),
]