from django.contrib import admin
from django.urls import path, include
from . import views




urlpatterns = [
    path('feseul/', views.FeseulView.as_view(), name='feseul'),
    path('feseul/<int:id>/', views.DetailView, name = 'details' ),
    path('feseulComment/', views.feseulComment, name='feseulComment'),
    # path('like_dislike', LikePost, name='like_dislike_post'),
    path("delete/<int:id>", views.DelPost, name='delpost'),
    path('search_post/', views.Search_post, name='search_post'),
    
]
