from django import forms

from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from .models import Client, DonneesPersonnelles, Address, ZipCode, City, Motorise, Voiture

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        # fields = '__all__'
        fields = ["nom_client", "prenom_client", "numero_afpa_client"]
        widgets = {
            'nom_client': TextInput(attrs={'class': 'form-control'}),
            'prenom_client': TextInput(attrs={'class': 'form-control'}),
            'numero_afpa_client': TextInput(attrs={'class': 'form-control'})
        }


class DonneesPersonnellesForm(forms.ModelForm):
    class Meta:
        model = DonneesPersonnelles
        fields = ["mail_client", "telephone_client"]
        widgets = {
            'mail_client': TextInput(attrs={'class': 'form-control'}),
            'telephone_client': TextInput(attrs={'class': 'form-control'})
        }  

    # Clean suivi du nom du champ concerné ensuite géré dans le Html
    def clean_mail_client(self):
        mail_client = self.cleaned_data['mail_client'].lower()
        r = DonneesPersonnelles.objects.filter(mail_client=mail_client)
        if r.count():
            raise  forms.ValidationError("Email existe déjà")
        return mail_client


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street"]
        widgets = {
            'street': TextInput(attrs={'class': 'form-control'})
        }

    # Clean suivi du nom du champ concerné ensuite géré dans le Html
    def clean_street(self):
        street = self.cleaned_data['street'].lower()
        r = Address.objects.filter(street=street)
        if r.count():
            raise  forms.ValidationError("l'adresse existe déjà")
        return street


class ZipCodeForm(forms.ModelForm):
    class Meta:
        model = ZipCode
        fields = ["zip_code"]
        widgets = {
            'zip_code': TextInput(attrs={'class': 'form-control'})
        }  


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ["city_name"]
        widgets = {
            'city_name': TextInput(attrs={'class': 'form-control'})
        }  

class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = '__all__'
        widgets = {
            'libelle_marque': TextInput(attrs={'class': 'form-control'}),
            'libelle_modele': TextInput(attrs={'class': 'form-control'}),
            'immatriculation': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'kilometrage': TextInput(attrs={'class': 'form-control'}),
            'date_mec': TextInput(attrs={'class': 'form-control'})
        }
       
