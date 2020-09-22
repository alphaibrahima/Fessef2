from django.contrib import admin
from django.urls import path, include
from . import  views




urlpatterns = [
    path('chat/', views.MessageView.as_view(), name='chat'),
    path('chat/<int:id>/', views.Inbox, name = 'inbox' ),
    
]
