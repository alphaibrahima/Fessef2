from django.db import models
from utilisateurs.models import User
from django.urls import reverse


# Create your models here.
class Feseul(models.Model):
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = "feseul_image", null=True, blank = True)
    #The easy way 
    likes     = models.ManyToManyField(User, related_name="likes", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    archive   = models.BooleanField(default=False)
    views     = models.IntegerField(default=0)
    contenu   = models.TextField()

    def __str__(self):
        return f"{self.author } --- {self.timestamp.date()}"
        # return self.author.username

    def get_absolute_url(self):
        return reverse("details", args=[self.id])
    
    def total_likes(self):
        return self.likes.count()




class FeseulComment(models.Model):
    comment = models.TextField()
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Feseul,  on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:13] + " ... " + " by  " + self.user.username





# class Like(models.Model):
#     user = models.ManyToManyField(User, related_name="linkingUser")
#     post = models.OneToOneField(Feseul, on_delete=models.CASCADE)

    

#     # Pour linker avec la classe "Feseul"
#     @classmethod
#     def like(cls, post, linking_user):
#         obj, create = cls.objects.get_or_create(post = post)
#         obj.user.add(linking_user)
#         # likes +=1


    
#     # Pour delinker avec la classe "Feseul"
#     @classmethod
#     def dislike(cls, post, dislinking_user):
#         obj, create = cls.objects.get_or_create(post = post)
#         obj.user.remove(dislinking_user)
        


#     def __str__(self):
#         return str(self.post)



    