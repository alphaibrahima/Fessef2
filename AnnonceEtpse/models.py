from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from utilisateurs.models import User


from django.db.models.signals import post_save, post_delete
from django.urls import reverse
from django.db import models
from notifications.models import Notification

from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager




class Post(models.Model):
    img_une     = models.ImageField(upload_to = "feseul_image", null=True, blank = True)
    likes       = models.ManyToManyField(User, related_name = "blog_posts")
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    body        = RichTextUploadingField(blank=True, null=True)
    slug        = models.SlugField(unique=True, max_length=100)
    timestamp   = models.DateTimeField(auto_now_add=True)
    description = RichTextField(blank=True, null=True)
    archive     = models.BooleanField(default=False)
    title       = models.CharField(max_length=255)
    views       = models.IntegerField(default=0)
    tags        = TaggableManager() 



    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
   


    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.title }  ||  {self.author}"
   
    def get_absolute_url(self):
        return reverse('annonce')


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user     

        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user     

        notify = Notification(post=post, sender=sender, user=post.user, notification_type=1)
        notify.delete()


post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_liked_post, sender=Likes)