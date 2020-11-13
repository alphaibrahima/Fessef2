from django.urls import path, include
from .views import * 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
# DetailsUtilisateurs


urlpatterns = [
    path('register', RetgistrationView.as_view(), name='register'),
    path('login', LotginView.as_view(), name='login'),
    path('profile', login_required(ProfileView.as_view()), name='profile'),
    path('editProfile', login_required(editpost), name='editProfile'),

    path('user/<int:id>/', DetailsUtilisateurs, name = 'userDetials' ),

    path('register_etpse', RetpsegistrationView.as_view(), name='register_etpse'),
    path('login_etpse', LoetpseginView.as_view(), name='login_etpse'),
    path('page', login_required(PageView.as_view()), name='page'),
    path('editPage', login_required(editpage), name='editPage'),
    path('searchPro', login_required(Search_Pro), name='searchPro'),

    path('register_assoc', RegistrationAssocView.as_view(), name='register_assoc'),
    path('page_asso', login_required(AssPageView.as_view()), name='page_asso'),
    path('login_assoc', LoginAssocView.as_view(), name='login_assoc'),
    path('editpageAss', login_required(editpageAss), name='editpageAss'),


    path('login_sene', LoginSeneView.as_view(), name='login_sene'),
    # path('reporting', login_required(ReportinView.as_view()), name='reporting'),

    path('social-auth/', include('social_django.urls', namespace="social")),

    path('logout', LogoutView.as_view(), name='logout'),

    path('', HomeView.as_view(), name='home'),

    path('activate/<uidb64>/<token>', ActivateAccountView.as_view(), name='activate'),
    # path('activate/<uidb64>/<token>', ActivateAccountView, name = 'activate' ),
    path('nouveau-password/<uidb64>/<token>', NouveauPasswordView.as_view(), name='nouveau-password'),
    path('request-reset-email', RequestResetEmailView.as_view(), name='request-reset-email'),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
]
