from django.contrib import admin
from django.urls import path, include
from .views import (AddCompeteView, DelCompet,)
# from notifications.views import  ShowNotifications


urlpatterns = [
    path('addcompete/', AddCompeteView.as_view(), name="addcompete"),
    path("delete/<int:id>", DelCompet, name='delcompet'),
]