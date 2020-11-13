from django.db import models
from django.urls import reverse
from utilisateurs.models import User, Profile
from django.template.defaultfilters import slugify
# Create your models here.

# Categories de competences
class CategoriCompetence(models.Model):
    slug    = models.SlugField(null=True, blank=True)
    titre   = models.CharField(max_length=150, null=False, blank=False)


    class Meta:
        verbose_name_plural = "CategoriesCompetence"
    
    # function for add slug
    def save(self, *args, **kwargs):
        self.slug = slugify(self.titre)
        super(CategoriCompetence, self).save(*args, **kwargs)

    def __str__(self):
        return self.titre

# Competences
class Compentence(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    profil = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(CategoriCompetence, related_name="competence", on_delete=models.CASCADE)

    def __str__(self):
        # return '%s %s' % (self.name, self.category , self.profil)
        return f"{self.profil } --- {self.name} --- {self.category}"