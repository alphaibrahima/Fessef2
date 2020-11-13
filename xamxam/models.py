from django.db import models
from django.urls import reverse
from utilisateurs.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager



class Category(models.Model):
    title     = models.CharField(max_length=255, default='Autre')
    slug      = models.SlugField()



    class Meta:
        verbose_name_plural = "Categories"
    
    # function for add slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Xamxam(models.Model):
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    category  = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to = "feseul_image", null=True, blank = True)
    views     = models.IntegerField(default=0, null=True, blank = True)
    slug      = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    archive   = models.BooleanField(default=False)
    title     = models.CharField(max_length=255)
    tags      = TaggableManager() 
    contenu   = models.TextField()


    # function for add slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Xamxam, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.author } -||- {self.timestamp.date()}"

    def get_absolute_url(self):
        # return reverse('annonce-datail', args=(str(self.id))) 
        return reverse('xamxam')