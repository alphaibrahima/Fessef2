from .models import *
from django import forms


class CompeteForm(forms.ModelForm):
    class Meta:

        model = Compentence 
        fields = ('profil', 'name', 'category')

        widgets = {
            'profil'  : forms.TextInput(attrs={'class' : 'form-control', 'value' : '', 'id' : 'username', 'type' : 'hidden' }),
            'name'    : forms.TextInput(attrs={'class' : 'form-control', 'label':'Competence :', 'placeholder': 'Competence'}),
            'category': forms.TextInput(attrs={'class' : 'form-control', 'label':'Categories :'}),
        }


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Compentence 
        fields = ('name', 'category')

        widgets = {
            'name'    : forms.TextInput(attrs={'class' : 'form-control', 'label':'Competence :', 'placeholder': 'Competence'}),
            'category': forms.TextInput(attrs={'class' : 'form-control', 'label':'Categories :'}),
        }
