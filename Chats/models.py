from django.db import models
from utilisateurs.models import User
from django.urls import reverse



class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name="reciever", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    contenu   = models.TextField()


    def __str__(self):
        return f"{self.sender } To {self.reciever} --- {self.timestamp.date()}"


