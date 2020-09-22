from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    is_etat         = models.BooleanField(default=False)
    is_student      = models.BooleanField(default=False)
    is_company      = models.BooleanField(default=False)
    is_association  = models.BooleanField(default=False)
    


class Profile(models.Model):
    cv                  = models.FileField(upload_to='CV/', null=True, blank=True)
    bio                 = models.TextField(max_length=500, blank=True)
    user                = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ville               = models.CharField(max_length=20, blank=True)
    # genre               = models.CharField(max_length=20, default="Homme", blank=True)
    linkedin            = models.URLField(max_length=250)
    thumbnail           = models.ImageField(default='users_profile/profile_default.jpg', upload_to='users_profile/', null=True, blank=True)
    update_to           = models.DateTimeField(auto_now_add=True)
    birth_date          = models.DateField( null=True, blank=True)
    phone_number        = models.CharField(max_length=30, blank=True, null=True)
    lettre_motivation   = models.FileField(upload_to='LM/', null=True, blank=True)
    
    #fond           = models.ImageField(default='users_profile/profile_default.jpg', upload_to='users_profile/', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.username, self.ville)


# Page pour les entreprises 
class Page(models.Model):
    thumbnail                   = models.ImageField(default='users_profile/profile_default.jpg', 
                                                    upload_to='Etpse_page/', null=True, blank=True)
    user                        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    domaine_dactivite           = models.TextField(max_length=200, blank=True)
    description                 = models.TextField(max_length=500, blank=True)
    phone_number                = models.CharField(max_length=12, blank=True)
    address                     = models.TextField(max_length=500, blank=True)
    update_to                   = models.DateTimeField(auto_now_add=True)
    date_creation_de_entreprise = models.DateField(null=True, blank=True )
    site_web                    = models.URLField(max_length=250)

    def __str__(self):
        return '%s %s' % (self.user.username, self.address)



# Page pour les Assciations 
class Association(models.Model):
    thumbnail                   = models.ImageField(default='users_profile/profile_default.jpg', 
                                                    upload_to='Assoc_page/', null=True, blank=True)
    user                        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    domaine_dactivite           = models.TextField(max_length=200, blank=True)
    description                 = models.TextField(max_length=500, blank=True)
    phone_number                = models.CharField(max_length=12, blank=True)
    address                     = models.TextField(max_length=500, blank=True)
    update_to                   = models.DateTimeField(auto_now_add=True)
    date_creation_association   = models.DateField(null=True, blank=True )
    site_web                    = models.URLField(max_length=250)

    def __str__(self):
        return '%s %s' % (self.user.username, self.address)
