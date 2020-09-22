from django.shortcuts import get_object_or_404, render,  redirect, HttpResponse
from django.views.generic import View
from django.contrib  import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from utilisateurs.models import *
from .models import *





class MessageView(View):

    def get(self, request):
        

        users = Message.objects.filter( Q(sender=request.user) | Q(reciever=request.user)
        ).order_by("-timestamp")    
        reception = Message.objects.all().order_by('-timestamp' )
        
        context  = {
            'users' : users,
            'reception':reception,

        }
        return render(request, 'chat/chatHome.html', context)


    def post(self, request):
        if request.method == 'POST':
            sender__    = request.user
            reciever__  = request.POST.get('receiver_id')
            contenu__   = request.POST.get('message')

            if reciever__:
                reciever_ = User.objects.get(id = reciever__)

            message = Message.objects.create(sender=sender__, reciever=reciever_, contenu=contenu__)
            message.save()

        # Checker si la requet est ajax 
            if request.is_ajax():
                print(" Ajax")

             

            return redirect('chat')



def Inbox(request, id):
    userId =  User.objects.get(id = id)
    connected_user = request.user

    if userId == connected_user:
        usersMsg = Message.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).order_by('timestamp')
    else:
        usersMsg = Message.objects.filter(Q(Q(sender=request.user) & Q(reciever=userId)) |
        Q(Q(sender=userId) & Q(reciever=request.user))).order_by('timestamp') 
    
    users = Message.objects.filter( Q(sender=request.user) | Q(reciever=request.user)
        ).order_by("-timestamp")
    
    reception = Message.objects.all().order_by('-timestamp' )

    # print(userId)

    context = {
        'receiverId' : userId,
        'inbox': usersMsg,
        'users' : users,
        'reception':reception,
    }

    # Voir si la requete est ajax
    if request.is_ajax():
        print('D Ajax')
        # si oui on envoi une reponse Json 
        # return JsonResponse(context, status = 200)
    return render(request, 'chat/chatHome.html', context)

           
            
            




       
            
            
      