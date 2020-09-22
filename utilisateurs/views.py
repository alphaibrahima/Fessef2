from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from .models import *
from Postfeeds.models import *
from AnnonceEtpse.models import *
from django.db.models import Q

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError

from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading



class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


# Class pour les inscriptions des etudiants
class RetgistrationView(View):
    def get(self, request):
        return render(request, 'etudiant/inscritpion.html')

    def post(self, request):

        context = {
            'data'      : request.POST,
            'has_error' : False
        }

        # Recuperation des datas 
        email       = request.POST.get('email')
        username    = request.POST.get('username')
        full_name   = request.POST.get('name')
        password    = request.POST.get('password')
        password2   = request.POST.get('password2')

        # Traitement de datas et gestion des messages d'erreur
        if len(password)<8:
            messages.add_message(request, messages.ERROR, 'Un Mot De Passe Doit Avoir Minimum 8 Lettres ')
            context['has_error']=True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Les Mots De Passes Ne Sont Pas Même')
            context['has_error']=True
          

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Veillez Renseigner Un Email Valide')
            context['has_error']=True


        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Username Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass


        if context['has_error']:
            return render(request, 'etudiant/inscritpion.html', context, status=400)
        
        # Sauvegarde dans la base de donnee
        
        user            = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name =   full_name
        user.last_name  =   full_name
        user.is_active  =   False
        user.is_student =   True

        user.save()
        Profile.objects.create(user=user)

        # Debut du systeme pour envoyer un mail
        current_site=get_current_site(request)
        email_subject='Active Your Account'
        message=render_to_string('activate.html',
        {
            'user'  :user,
            'domain':current_site.domain,
            'uid'   :urlsafe_base64_encode(force_bytes(user.pk)),
            'token' :generate_token.make_token(user)
        }
        )

        email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        )
        EmailThread(email_message).start()
        # email_message.send()

        messages.add_message(request, messages.SUCCESS, 'Lien D\'activation envoyé Avec Success')
        return redirect('login')


# 
# Inscription pour les entreprise
# 

class RetpsegistrationView(View):
    def get(self, request):
        return render(request, 'etpse/registration.html')

    def post(self, request):

        context = {
            'data'      : request.POST,
            'has_error' : False
        }

        # Recuperation des datas 
        email       = request.POST.get('email')
        username    = request.POST.get('username')
        # full_name   = request.POST.get('name')
        password    = request.POST.get('password')
        password2   = request.POST.get('password2')

        # Traitement de datas et gestion des messages d'erreur
        if len(password)<8:
            messages.add_message(request, messages.ERROR, 'Un Mot De Passe Doit Avoir \n Minimum 8 Lettres ')
            context['has_error']=True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Les Mots De Passes Ne Sont Pas Même')
            context['has_error']=True
          

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Veillez Renseigner Un Email Valide')
            context['has_error']=True


        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Ce Nom  Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass


        if context['has_error']:
            return render(request, 'etpse/registration.html', context, status=400)
        
        # Sauvegarde dans la base de donnee
        
        user            = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        # user.first_name =   full_name
        # user.last_name  =   full_name
        user.is_active  =   False
        user.is_company =   True

        user.save()
        Page.objects.create(user=user)

        # Debut du systeme pour envoyer un mail
        current_site=get_current_site(request)
        email_subject='Active Your Account'
        message=render_to_string('activate.html',
        {
            'user'  :user,
            'domain':current_site.domain,
            'uid'   :urlsafe_base64_encode(force_bytes(user.pk)),
            'token' :generate_token.make_token(user)
        }
        )

        email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
        )
        EmailThread(email_message).start()
        # email_message.send()

        messages.add_message(request, messages.SUCCESS, 'Lien D\'activation envoyé Avec Success')
        return redirect('login_etpse')





# Class pour l'activation de compte
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            messages.add_message(request, messages.INFO, 'Compte Activé  Avec Succes')
            if user.is_student :
                return redirect('login')
            elif user.is_company :
                return redirect('login_etpse')
        return render(request, 'activate_failed.html',status=401)




# Class pur traiter la connexion et gerer les erreurs
class LotginView(View):
    def get(self, request):
        return render(request, 'etudiant/login.html')

    def post(self, request):
        context = {
            'data'      : request.POST,
            'has_error' : False
        }
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'Username Est Requis')
            context['has_error']=True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Password Est Requis')
            context['has_error']=True
        user=authenticate(request,username=username,password=password)
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Le Login Est Invalid')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'etudiant/login.html', status=401,context=context)
        login(request, user)
        return redirect('home')
        return render(request, 'etudiant/login.html')



# 
# Connexion pour les entreprise
# 
class LoetpseginView(View):
    def get(self, request):
        return render(request, 'etpse/registration.html')

    def post(self, request):
        context = {
            'data'      : request.POST,
            'has_error' : False
        }
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'Nom d\'entreprise Est Requis')
            context['has_error']=True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Mots de passe est requis')
            context['has_error']=True
        user=authenticate(request,username=username,password=password)
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Le Login Est Invalid')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'etpse/registration.html', status=401,context=context)
        login(request, user)
        return redirect('home')
        return render(request, 'etpse/registration.html')




class LoginSeneView(View):
    def get(self, request):
        return render(request, 'etat_senegal/login.html')

    def post(self, request):
        context = {
            'data'      : request.POST,
            'has_error' : False
        }
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'Le Nom D\'utilisateur Est Requis')
            context['has_error']=True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Le Mots De Passe Est Requis')
            context['has_error']=True
        user=authenticate(request,username=username,password=password)
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Les identifiants  sont Invalid')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'etat_senegal/login.html', status=401,context=context)
        login(request, user)
        return redirect('reporting')
        return render(request, 'etat_senegal/login.html')







class LoginAssocView(View):
    def get(self, request):
        return render(request, 'association/login.html')

    def post(self, request):
        context = {
            'data'      : request.POST,
            'has_error' : False
        }
        username    = request.POST.get('username')
        password    = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR, 'Username Est Requis')
            context['has_error']=True
        if password == '':
            messages.add_message(request, messages.ERROR, 'Password Est Requis')
            context['has_error']=True
        user=authenticate(request,username=username,password=password)
        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Le Login Est Invalid')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'association/login.html', status=401,context=context)
        login(request, user)
        return redirect('home')
        return render(request, 'association/login.html')



class RegistrationAssocView(View):
    def get(self, request):
        return render(request, 'association/registration.html')

    def post(self, request):

        context = {
            'data'      : request.POST,
            'has_error' : False
        }

        # Recuperation des datas 
        email       = request.POST.get('email')
        username    = request.POST.get('username')
        # full_name   = request.POST.get('name')
        password    = request.POST.get('password')
        password2   = request.POST.get('password2')

        # Traitement de datas et gestion des messages d'erreur
        if len(password)<8:
            messages.add_message(request, messages.ERROR, 'Un Mot De Passe Doit Avoir \n Minimum 8 Lettres ')
            context['has_error']=True

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Les Mots De Passes Ne Sont Pas Même')
            context['has_error']=True
          

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Veillez Renseigner Un Email Valide')
            context['has_error']=True


        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR, 'Ce Nom  Existe Déjà ') 
                context['has_error']=True
        except Exception as identifier:
            pass


        if context['has_error']:
            return render(request, 'association/registration.html', context, status=400)
        
        # Sauvegarde dans la base de donnee
        
        user            = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        # user.first_name =   full_name
        # user.last_name  =   full_name
        user.is_active  =   False
        user.is_association =   True

        user.save()
        Association.objects.create(user=user)

        # Debut du systeme pour envoyer un mail
        current_site=get_current_site(request)
        email_subject='Active Your Account'
        message=render_to_string('activate.html',
        {
            'user'  :user,
            'domain':current_site.domain,
            'uid'   :urlsafe_base64_encode(force_bytes(user.pk)),
            'token' :generate_token.make_token(user)
        }
        )

        email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email]
        )
        EmailThread(email_message).start()
        # email_message.send()

        messages.add_message(request, messages.SUCCESS, 'Lien D\'activation envoyé Avec Success')
        return redirect('login_assoc')



# Class pour LA page d'accueil
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


# Class pour la deconnexion 
class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Vous Etes Deconnecté')
        return redirect('login')



# Class pour le reset email 
class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'reset-email.html' )
    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'L\'email entré n\'est pas valid')
            return render(request, 'reset-email.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset your Password]'
            message = render_to_string('reset-user-password.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0])
                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, 'We have sent you an email with instructions on how to reset your password')
        return render(request, 'reset-email.html')
# 
class NouveauPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Password reset link, is invalid, please request a new one')
                return render(request, 'reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            
            messages.success(
                request, 'Invalid link')
            return render(request, 'reset-email.html')

        return render(request, 'set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 8:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be at least 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords don`t match')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, 'Password reset success, you can login with new password')

            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
           
            messages.error(request, 'Something went wrong')
            return render(request, 'set-new-password.html', context)

        return render(request, 'set-new-password.html', context)


#Gestion de profile

class ProfileView(View):
    def get(self, request):
        post = Feseul.objects.filter(author=request.user)
        postall = Post.objects.all()
        context = {
            'posts' : post,
            'postall': postall,
        }
        return render(request, 'etudiant/profile.html', context)


class EditProfileView(View):
    def get(self, request):
        return render(request, 'etudiant/editprofile.html')

def editpost(request):
    data = Profile.objects.get(user__id = request.user.id)
    data = {
        'data' : data,
    }
    if request.method == 'POST':
        username_       = request.POST.get('username')
        linkedin_       = request.POST.get('linkedin')
        phone_          = request.POST.get('tel')
        email_          = request.POST.get('email')
        name_           = request.POST.get('name')
        ville_          = request.POST.get('ville')
        tel_            = request.POST.get('tel')
        bio_            = request.POST.get('bio')   

        user__id = request.user.id
        user     = get_object_or_404(User, id=user__id)

        user.first_name = name_
        user.username  = username_ 
        user.last_name  = name_
        user.email      = email_
        user.save()

        
        user = get_object_or_404(Profile, user_id=user__id) 
        user.phone_number = phone_
        user.linkedin = linkedin_
        user.ville = ville_
        user.bio = bio_
        user.save()
        
        if "birth_date" in request.FILES:
            birth_date_ = request.FILES['birth_date']
            user.birth_date = birth_date_
            user.save()
        
        if "thumbnail" in request.FILES:
            thumbnail_ = request.FILES['thumbnail']
            user.thumbnail = thumbnail_
            user.save()

        if "cv_" in request.FILES:
            cv_ = request.FILES['cv']
            user.cv = cv_
            user.save()

        if "lm" in request.FILES:
            lm__ = request.FILES['lm']
            user.lettre_motivation = lm__
            user.save()
        messages.add_message(request, messages.SUCCESS, 'Profile mis à jour  Avec Succes')
        return redirect('profile')
    return render(request, 'etudiant/editprofile.html')

class PageView(View):
    def get(self, request):
        postall    = Post.objects.all()
        last       = Post.objects.order_by('-timestamp')[0:3]
        post       = Post.objects.filter(author=request.user)
        
        context = {
            'postall'    : postall,
            'posts'      : post,
            'last'       : last,
        }
        return render(request, 'etpse/page.html', context)

class EditPageView(View):
    def get(self, request):
        return render(request, 'etpse/editpage.html')

def editpage(request):
    data = Page.objects.get(user__id = request.user.id)
    data = {
        'data' : data,
    }
    if request.method == 'POST':
        domaineactivite_= request.POST.get('domaineactivite')
        username_       = request.POST.get('username')
        # birth_date_     = request.POST.get('birth_date')
        address_        = request.POST.get('address')
        site_           = request.POST.get('site')
        phone_          = request.POST.get('tel')
        email_          = request.POST.get('email')
        tel_            = request.POST.get('tel')
        bio_            = request.POST.get('bio')   

        user__id = request.user.id
        user     = get_object_or_404(User, id=user__id) 

        user.username  = username_ 
        user.email     = email_
        user.save()

        user     = get_object_or_404(Page, user_id=user__id) 
        
        # user.date_creation_de_entreprise = birth_date_
        user.domaine_dactivite           = domaineactivite_
        user.phone_number                = phone_
        user.description                 = bio_
        user.site_web                    = site_
        user.address                     = address_
        user.save()

        if "birth_date" in request.FILES:
            birth_date_                      = request.FILES['birth_date']
            user.date_creation_de_entreprise = birth_date_
            user.save()
        
        if "thumbnail" in request.FILES:
            thumbnail_ = request.FILES['thumbnail']
            user.thumbnail = thumbnail_
            user.save()


        messages.add_message(request, messages.SUCCESS, 'Page mis à jour  Avec Succes')
        return redirect('page')
    return render(request, 'etpse/editpage.html')


# Pages d'association 
class AssPageView(View):
    def get(self, request):
        postall = Post.objects.all()
        last    = Post.objects.order_by('-timestamp')[0:3]
        post    = Post.objects.filter(author=request.user)
        context = {
            'postall': postall,
            'posts'  : post,
            'last': last,
        }
        return render(request, 'association/pages.html', context)



# Gestgion de la page
class EditAssPageView(View):
    def get(self, request):
        return render(request, 'association/updatepages.html')

def editpageAss(request):
    data = Association.objects.get(user__id = request.user.id)
    data = {
        'data' : data,
    }

    if request.method == 'POST':
        domaineactivite_= request.POST.get('domaineactivite')
        username_       = request.POST.get('username')
        # birth_date_     = request.POST.get('birth_date')
        address_        = request.POST.get('address')
        site_           = request.POST.get('site')
        phone_          = request.POST.get('tel')
        email_          = request.POST.get('email')
        tel_            = request.POST.get('tel')
        bio_            = request.POST.get('bio')   

        user__id = request.user.id
        user     = get_object_or_404(User, id=user__id) 
        
         
        user.username  = username_ 
        user.email     = email_
        user.save()
        

        
        user     = get_object_or_404(Association, user_id=user__id)
        # user.date_creation_de_entreprise = birth_date_
        user.domaine_dactivite           = domaineactivite_
        user.phone_number                = phone_
        user.description                 = bio_
        user.site_web                    = site_
        user.address                     = address_
        user.save()
        

        if "birth_date" in request.FILES:
            birth_date_                    = request.FILES['birth_date']
            user.date_creation_association = birth_date_
            user.save()
        
        if "thumbnail" in request.FILES:
            thumbnail_ = request.FILES['thumbnail']
            user.thumbnail = thumbnail_
            user.save()

            print(user.thumbnail)


        messages.add_message(request, messages.SUCCESS, 'Page mis à jour  Avec Succes')
        return redirect('page_asso')
    return render(request, 'association/updatepages.html')




def Search_Pro(request):
    search_query = request.GET.get('search')
    if search_query:
        posts = Profile.objects.filter(Q(ville__icontains = search_query)|
        Q(user__username__icontains=search_query)  )
        
    context = {
    'posts': posts
    }
    return render(request, 'etpse/search_profile.html', context)
            
            






