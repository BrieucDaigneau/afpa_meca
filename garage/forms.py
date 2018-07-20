from django import forms

from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from .models import Client, DonneesPersonnelles


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        # fields = '__all__'
        fields = ["nom_client", "prenom_client"]
        widgets = {
            'nom_client': TextInput(attrs={'class': 'form-control'}),
            'prenom_client': TextInput(attrs={'class': 'form-control'})
        }


class DonneesPersonnellesForm(forms.ModelForm):
    class Meta:
        model = DonneesPersonnelles
        fields = ["mail_client", "telephone_client"]
        widgets = {
            'mail_client': TextInput(attrs={'class': 'form-control'}),
            'telephone_client': TextInput(attrs={'class': 'form-control'})
        }  
