from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import View
from django.contrib  import messages
from django.urls import reverse
from django.db.models import Q
# from django.urls import reverse
from AnnonceEtpse.models import *
from Postfeeds.templatetags import extras
from .models import *
from .forms import *
import json

# Create your views here.

class FeseulView(View):
    def get(self, request):
        posts   = Feseul.objects.all().order_by('-timestamp' )
        postss  = Post.objects.all().order_by('-timestamp' )
        context = {
            'posts' : posts,
            'postss': postss,
        }

        # if request.is_ajax():
        #     print(" tesst ")
        #     return JsonResponse({'data': list(posts.values()), 'data2': list(postss.values()),})
        return render(request, 'PostFeeds/postfeed.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            contenu_       = request.POST.get('text')
            author_        = request.user

            fesseul_obj    = Feseul(author=author_, contenu=contenu_)
            fesseul_obj.save()

            if "image" in request.FILES:
                thumbnail_     = request.FILES['image']

                fesseul_obj.thumbnail = thumbnail_
                fesseul_obj.save()

            messages.success(request, " Feseul avec success : ")
            return redirect('feseul')
        else:
            messages.error(request, "Quelque Chose ne va pas :")
            return redirect('feseul')




def DetailView(request, id):
    post = Feseul.objects.get(id=id)
    print(post)
    post.views = post.views + 1
    post.save()

    comments        = FeseulComment.objects.filter(post=post, parent=None).order_by('timestamp')
    replies         = FeseulComment.objects.filter(post=post).exclude(parent=None).order_by('timestamp')
    total_comments  = FeseulComment.objects.filter(post=post)
    replyDict = {}
    for reply in replies:
        if reply.parent.id not in replyDict.keys() : 
            replyDict[reply.parent.id] = [reply]
        else:
            replyDict[reply.parent.id].append(reply)

    # if request.method == 'POST':
    #     comment_form = CommentForm(request.POST or None)
    #     if comment_form.is_valid():
    #         content = request.POST.get('contenu')
    #         reply_id = request.POST.get('comment_id')
    #         comment_qs = None
    #         if reply_id:
    #             comment_qs = Comment.objects.get(id = reply_id)
    #         comment = Comment.objects.create(post=post, user=request.user, contenu=content, reply=comment_qs)
    #         comment.save()


            # return redirect(reverse("details", kwargs={
            #     'id': post.pk
            # }))
            # return HttpResponseRedirect(post.get_absolute_url())
    # else:
    #     comment_form = CommentForm()

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'post'           : post,
        'replyDict'      : replyDict,
        'comments'       : comments,
        'is_liked'       : is_liked,
        'total_comments' : total_comments,
        'total_like'     : post.total_likes(),
     }
    # if request.is_ajax():
    #     html = render_to_string('partials/_comments.html', context, request=request)
    #     return JsonResponse({'form': html})

    return render(request, 'PostFeeds/detailpost.html', context)


def feseulComment(request):
    if request.method == 'POST':
        comment_  = request.POST.get('comment')
        print(comment_)
        user_  = request.user
        print(user_)
        postId_  = request.POST.get('postId')
        post_ = Feseul.objects.get(id=postId_)
        print(post_)
        parentId_ = request.POST.get('parentId')
        print(parentId_)
    
        if parentId_ == "":
            comment = FeseulComment(comment=comment_, user=user_, post=post_)
            comment.save()
        else :
            parent_ = FeseulComment.objects.get(id=parentId_)
            comment = FeseulComment(comment=comment_, user=user_, post=post_, parent=parent_)

            comment.save()
        

    return redirect(post_.get_absolute_url())











def like_post(request):
    post = get_object_or_404(Feseul, id=request.POST.get('post_id'))
    # post = get_object_or_404(Feseul, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    # if request.is_ajax():
    #     html = render_to_string('partials/_like.html', context, request=request)
    #     return JsonResponse({'form': html})

    return HttpResponseRedirect(post.get_absolute_url())









def DelPost(request, id):
    # post_ = Feseul.objects.filter(pk=id)
    post_ = get_object_or_404(Feseul, id=id)
    post_.delete()
    return redirect('feseul')


def Search_post(request):
    search_query = request.GET.get('search')
    if search_query:
        posts = Feseul.objects.filter(Q(author__username__icontains = search_query)|
        Q(contenu__icontains=search_query))
        
    context = {
    'posts': posts
    }
    return render(request, 'PostFeeds/resultat_search.html', context)






# def LikePost(request):
#     post_id = request.GET.get("likeId", "") # feseul id
#     print(post_id)
#     post = Feseul.objects.get(pk=post_id) # post obj
#     user = request.user
#     like = Like.objects.filter(post = post, user = user)
#     liked = False
#     if like:
#         Like.dislike(post, user)
#     else:
#         liked = True
#         Like.like(post, user)
#     resp = {
#         "liked" : liked
#     }
#     response = json.dumps(resp)
#     return HttpResponse(response, content_type ="application/json")