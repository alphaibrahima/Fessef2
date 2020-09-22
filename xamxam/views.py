from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import( ListView, 
                CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse
from .forms import XamxamForm, UpdateForm
from .models import Xamxam


# fonction pour Ajouter un post xamxam
class AddXamxam(CreateView):
    model           =  Xamxam
    form_class      =  XamxamForm
    template_name   = 'xamxam/addxamxam.html'




# fonction pour modifier son post xamxam
class UpdateXamxamView(UpdateView):
    model           =  Xamxam
    form_class      =  UpdateForm
    template_name   = 'xamxam/updatexamxam.html' 
    # fields = ['title', 'thumbnail', 'contenu']






# Fonction pour avoir tous les posts xamxam
class XamxamView(ListView):
    
    model = Xamxam
    template_name = 'xamxam/xamaxam.html'
    ordering = ['-timestamp']
    context_object_name = 'xamaAll'

    

# Pour avoir les details de l'article
def XamxaDetailView(request, id):
    post = Xamxam.objects.get(id=id)
    post.views = post.views + 1
    post.save()

    context = {
        'post' : post,
    }

    return render(request, 'xamxam/xamDetails.html', context)







# suprimer un post xamxam
def DelXamxam(request, id):
    post_ = get_object_or_404(Xamxam, id=id)
    post_.delete()
    return redirect('xamxam')