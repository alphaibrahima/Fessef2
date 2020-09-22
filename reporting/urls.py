from django.urls import path
from .views import * 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('reporting', login_required(ReportinView.as_view()), name='reporting'), 
]
