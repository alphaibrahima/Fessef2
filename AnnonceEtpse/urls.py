from django.contrib import admin
from django.urls import path
from .views import (AnnonceView, AnnonceDetailView, 
        AddAnnonceView, AnnonceUpdateView, DeleteAnnonceView,
         LikeView, Search, Tagged)




urlpatterns = [
    path('annonce/', AnnonceView.as_view(), name="annonce"),
    path('annonce/<int:pk>', AnnonceDetailView.as_view(), name="annonce-datail"),
    path('annonce/tag/<slug:slug>/', Tagged, name="tagged"),
    path('addannonce/', AddAnnonceView.as_view(), name="add-annonce"),
    # path('addcategory/', AddCategoryView.as_view(), name="add-category"),
    path('annonce/edit/<int:pk>', AnnonceUpdateView.as_view(), name="update-annonce"),
    path('annonce/<int:pk>/suprimer', DeleteAnnonceView.as_view(), name="delete-annonce"),
    # path('category/<str:cats>/', CategoryView, name = 'category'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('search/', Search, name='search'),
    
]
