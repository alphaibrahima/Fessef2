from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View

from .models import *
from Postfeeds.models import *
from AnnonceEtpse.models import *
from utilisateurs.models import *
from django.db.models import Q





# Create your views here.
class ReportinView(View):
    def get(self, request):
        postfeed   = Feseul.objects.all()
        posts      = Post.objects.all()
        users      = User.objects.all()
        profiles   = Profile.objects.all()
        pages      = Page.objects.all()

        context = {
            'postfeed' : postfeed,
            'profiles': profiles,
            'posts': posts,
            'users': users,
            'pages': pages,
        }

        return render(request, 'etat_senegal/reporting.html', context)