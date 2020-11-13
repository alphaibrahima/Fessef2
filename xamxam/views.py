from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import( ListView, 
                CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse
from .forms import XamxamForm, UpdateForm
from taggit.models import Tag
from .models import Xamxam, Category




def Taggedd(request, slug):
    tag                 = get_object_or_404(Tag, slug=slug)
    posts               = Xamxam.objects.filter(tags = tag)
    common_Tags         = Xamxam.tags.most_common()[:10]
    context             = {
        'tag'         : tag,
        'posts'       : posts,
        'common_Tags' : common_Tags
    }
    return render(request, 'xamxam/xamaxam.html', context)




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
    context_object_name = 'posts'

    

# Pour avoir les details de l'article
def XamxaDetailView(request, id):
    post = Xamxam.objects.get(id=id)
    post.views = post.views + 1
    post.save()

    context = {
        'post' : post,
    }

    return render(request, 'xamxam/xamDetails.html', context)


#categori
def category(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'category' : category
    }
    return render(request, 'xamxam/category.html', context)







# suprimer un post xamxam
def DelXamxam(request, id):
    post_ = get_object_or_404(Xamxam, id=id)
    post_.delete()
    return redirect('xamxam')