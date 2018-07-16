from django import forms

from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from .models import Client 

class ClientForm(forms.Form):
    nom_client = forms.CharField(
        label='Nom',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )

    prenom_client = forms.CharField(
        label='Prenom_client',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )     

    # telephone_client = forms.CharField(
    #     label='telephone',
    #     max_length=15,
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     required=True
    #     )      

    # email_client = forms.EmailField(
    #     label='email',
    #     max_length=50,
    #     widget=forms.EmailInput(attrs={'class': 'form-control'}),
    #     required=True)   

    # adresse_client = forms.CharField(
    #     label='adresse',
    #     max_length=100,
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     required=True
    #     )        

    # code_postal_client = forms.IntegerField(
    #     label='code_postal',
    #     widget=forms.TextInput(attrs={'class': 'form-control'}),
    #     required=True
    #     )        
        
    # ville_client = forms.CharField(
    #     label='ville',
    #     widget=forms.TextInput(attrs={'class': 'custom-select d-block w-100'}),
    #     required=True
    #     )   

    # pays_client = forms.CharField(
    #     label='pays',
    #     widget=forms.TextInput(attrs={'class': 'custom-select d-block w-100'}),
    #     required=True
    #     )                               







