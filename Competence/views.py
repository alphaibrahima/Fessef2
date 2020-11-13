from .models import *
from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse


class AddCompeteView(View):
    def get(self, request):
        posts   = CategoriCompetence.objects.all()
        context = {
            'posts' : posts,
        }

        if request.is_ajax():
            return JsonResponse({'data': list(posts.values())})
        # return render(request, 'etudiant/profile.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            name_          = request.POST.get('compentence')
            # categorie_     = request.POST.get('categorie')
            profil_        = request.user.profile


            categorie_  = CategoriCompetence.objects.get(id=request.POST.get('categorie'))
            compete_obj    = Compentence.objects.create(profil=profil_, name=name_, category=categorie_)
            compete_obj.save()
            return redirect('profile')
        else:
            messages.error(request, "Quelque Chose ne va pas !!!!!")
            return redirect('profile')


def DelCompet(request, id):
    # post_ = Feseul.objects.filter(pk=id)
    compet_ = get_object_or_404(Compentence, id=id)
    compet_.delete()
    return redirect('profile')