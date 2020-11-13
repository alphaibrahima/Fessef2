from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('contenu',)

admin.site.register(Category)
admin.site.register(Xamxam, SomeModelAdmin)
