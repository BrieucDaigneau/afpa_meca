from django import forms

from django.forms import ModelForm, TextInput, EmailInput, SelectDateWidget, FileInput, NumberInput, DateInput, Textarea
from django.forms.utils import ErrorList
from .models import Client, DonneesPersonnelles, Address, ZipCode, City, Motorise, Voiture, Intervention, Moto, Velo

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        # fields = '__all__'
        fields = ["nom_client", "prenom_client", "numero_afpa_client"]
        widgets = {
            'nom_client': TextInput(attrs={'class': 'form-control'}),
            'prenom_client': TextInput(attrs={'class': 'form-control'}),
            'numero_afpa_client': NumberInput(attrs={'class': 'form-control'})
        }


class DonneesPersonnellesForm(forms.ModelForm):
    class Meta:
        model = DonneesPersonnelles
        fields = ["mail_client", "telephone_client","carte_AFPA_img"]
        widgets = {
            'mail_client': TextInput(attrs={'class': 'form-control'}),
            'telephone_client': TextInput(attrs={'class': 'form-control'}),
            'carte_AFPA_img': FileInput(attrs={'class': 'form-control'})
        }  

    # Clean suivi du nom du champ concerné ensuite géré dans le Html
    # def clean_mail_client(self):
    #     mail_client = self.cleaned_data['mail_client'].lower()
    #     r = DonneesPersonnelles.objects.filter(mail_client=mail_client)
    #     if r.count():
    #         raise  forms.ValidationError("Email existe déjà")
    #     return mail_client


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street","street_number","street_complement"]
        widgets = {
            'street': TextInput(attrs={'class': 'form-control'}),
            'street_number': NumberInput(attrs={'class': 'form-control'}),
            'street_complement': TextInput(attrs={'class': 'form-control'})
        }

    # Clean suivi du nom du champ concerné ensuite géré dans le Html
    # def clean(self):
    #     cleaned_data = super().clean()
    #     street_number = self.cleaned_data['street_number']
    #     street = self.cleaned_data['street']
    #     r = Address.objects.filter(street_number=street_number,street=street)
    #     if r.count():
    #         raise forms.ValidationError("l'adresse existe déjà")
    #     return cleaned_data


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
        exclude = ('client', 'carte_grise_img', 'carte_assurance_img', 'type_vehicule' )
        widgets = {
            'libelle_marque': TextInput(attrs={'class': 'form-control'}),
            'libelle_modele': TextInput(attrs={'class': 'form-control'}),
            'immatriculation': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'kilometrage': NumberInput(attrs={'class': 'form-control'}),
            'date_mec': DateInput(attrs={'class': 'form-control'}),
            'carte_grise_img': FileInput(attrs={'class': 'form-control'}),
            'carte_assurance_img': FileInput(attrs={'class': 'form-control'})
        }
class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        exclude = ('client', 'carte_grise_img', 'carte_assurance_img', 'type_vehicule'  )
        widgets = {
            'libelle_marque': TextInput(attrs={'class': 'form-control'}),
            'libelle_modele': TextInput(attrs={'class': 'form-control'}),
            'immatriculation': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'kilometrage': NumberInput(attrs={'class': 'form-control'}),
            'date_mec': DateInput(attrs={'class': 'form-control'}),
            'carte_grise_img': FileInput(attrs={'class': 'form-control'}),
            'carte_assurance_img': FileInput(attrs={'class': 'form-control'})
        }

class VeloForm(forms.ModelForm):
    class Meta:
        model = Velo
        fields = ['libelle_modele']
        widgets = {
            'libelle_modele': TextInput(attrs={'class': 'form-control'}),
        }

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        exclude = ('intervention_realisee', 'statut', 'utilisateur', 'vehicule', 'date_saisie_intervention')
        widgets = {
            'date_restitution_prevu': DateInput(attrs={'class': 'form-control'}),    
            'diagnostic' : Textarea(attrs={'class': 'form-control'}),  
            'intervention_a_realiser' : Textarea(attrs={'class': 'form-control'}),
        }




