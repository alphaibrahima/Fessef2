from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification

# Create your views here.

def ShowNotifications(request):
    user          = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')

    template      = loader.get_template('notifications/associationNotify.html')

    context       = {
        'notifications': notifications,
    }
    return HttpResponse(template.render(context, request))
