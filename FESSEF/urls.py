from django.contrib import admin
from django.urls import path, include
from Postfeeds import views
from django.conf import settings 
from django.conf.urls.static import static

admin.site.site_header = "Fessef"
admin.site.site_title = "Fessef Admin Panel"
admin.site.index_title = "Bienvenue dans Fessef Admin Panel"




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('like/', views.like_post, name='like_post'),
    path('Chats/', include('Chats.urls'), name='Chats'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('xamxam/', include('xamxam.urls'), name='xamxam'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('reporting/', include('reporting.urls'), name='reporting'),
    path('postfeeds/', include('Postfeeds.urls'), name='postfeeds'),
    path('Competence/', include('Competence.urls'), name='Competence'),
    path('annonceEtpse/', include('AnnonceEtpse.urls'), name='annonceEtpse'),
    path('notifications/', include('notifications.urls'), name='notifications'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)