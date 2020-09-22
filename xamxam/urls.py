from django.contrib import admin
from django.urls import path, include
from . import views




urlpatterns = [
    path('xamxam/', views.XamxamView.as_view(), name='xamxam'),
    path("addxamxam/", views.AddXamxam.as_view(), name='addxamxam'),
    path("sup/<int:id>", views.DelXamxam, name='delxamxam'),
    path('xamxam/<int:id>/', views.XamxaDetailView, name = 'Xdetails' ),
    # path("update/<int:id>", views.UpdateXamxam, name='updatexamxam'),
    path('xamxam/edit/<int:pk>/', views.UpdateXamxamView.as_view(), name = 'updatexamxam'),
    
]