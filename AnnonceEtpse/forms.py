from django import forms
from .models import Post




class AnnonceForm(forms.ModelForm):
    class Meta:

        model = Post 
        fields = ('title', 'tags', 'img_une', 'author','description',  'body')

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'label':'Titre :', 'placeholder': 'Entrez votre titre...'}),
            'tags' : forms.TextInput(attrs={'class' : 'form-control',   'type' : 'text', 'data-role' : 'tagsinput' }),
            'author' : forms.TextInput(attrs={'class' : 'form-control', 'value' : '', 'id' : 'username', 'type' : 'hidden' }),
            'description' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Entrez Une Description ...'}),
            'body' : forms.Textarea(attrs={'class' : 'form-control'}),

        }


class UpdateForm(forms.ModelForm):
    class Meta:

        model = Post 
        fields = ('title','tags', 'img_une', 'description',   'body')

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Entrez votre titre...'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder': 'Entrez Une Description ...'}),
            'body' : forms.Textarea(attrs={'class' : 'form-control'}),
            
        }

        