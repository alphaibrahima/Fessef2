from django.shortcuts import render, get_object_or_404
from django.views.generic import( ListView, DetailView, 
                CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from .forms import AnnonceForm, UpdateForm
from .models import Post
from django.template.defaultfilters import slugify
from taggit.models import Tag
from django.db.models import Q




def Tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags = tag)
    common_Tags         = Post.tags.most_common()[:10]
    context = {
        'tag'         : tag,
        'posts'       : posts,
        'common_Tags' : common_Tags
    }
    return render(request, 'etpse/home.html', context)



class AnnonceView(ListView):
    
    model = Post
    template_name       = 'etpse/home.html'
    ordering            = ['-timestamp']
    last                = Post.objects.order_by('-timestamp')[0:3]
    context_object_name = 'posts'
    
        

def Search(request):
    search_query = request.GET.get('search')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains = search_query)|
        Q(body__icontains=search_query) | Q(author__username__icontains=search_query) | 
        Q(tags__icontains=search_query)
        
        )
        
        context = {
            'posts': posts
        }
    return render(request, 'etpse/search_resultat.html', context)



def LikeView(request, pk):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    #     # debtut de ligne Json
    #     return JsonResponse({"success":True}, status=200)
    # return JsonResponse({"success":False}, status=400)
    return HttpResponseRedirect(reverse('annonce-datail', args=[str(pk)]))





class AnnonceDetailView(DetailView):
    model=Post
    template_name = 'etpse/details.html'
    def get_context_data(self, *args, **kwargs):
        context = super(AnnonceDetailView, self).get_context_data(*args, **kwargs)
       
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        stuff.views = stuff.views + 1
        stuff.save()
        
        print(stuff)
        total_likes = stuff.total_likes() 

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        
        return context
    


class AddAnnonceView(CreateView):
    model           =  Post
    form_class      =  AnnonceForm
    template_name   = 'etpse/addannonce.html'



class AnnonceUpdateView(UpdateView):
    model           =  Post
    form_class      =  UpdateForm
    template_name   = 'etpse/updateannonce.html' 

class DeleteAnnonceView(DeleteView):
    model = Post 
    template_name = 'etpse/deleteannonce.html'
    success_url = reverse_lazy('annonce')
    