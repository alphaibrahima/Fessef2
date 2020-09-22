from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Xamxam
from django import forms





class XamxamForm(forms.ModelForm):
    class Meta:

        model = Xamxam 
        fields = ('author', 'thumbnail', 'title',  'contenu')

        widgets = {
            'author' : forms.TextInput(attrs={'class' : 'form-control', 'value' : '', 'id' : 'username', 'type' : 'hidden' }),
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'label':'Titre :', 'placeholder': 'Entrez votre titre...'}),
            # 'contenu' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Entrez Le contenu...'}),
            'contenu' : SummernoteWidget(),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Xamxam 
        fields = ('thumbnail', 'title', 'contenu')

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Entrez votre titre...'}),
            # 'contenu' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Entrez Le contenu...'}),
            'contenu' : SummernoteWidget(),   
        }

        