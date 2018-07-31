from django import forms

from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from .models import Client, DonneesPersonnelles, Address, ZipCode, City

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
            raise  forms.ValidationError("Email already exists")
        return mail_client


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street"]
        widgets = {
            'street': TextInput(attrs={'class': 'form-control'})
        }



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


class LogoutForm(forms.Form):
    pass
