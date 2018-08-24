from django import forms
from django.forms import ModelForm, TextInput, EmailInput, SelectDateWidget, FileInput, NumberInput, DateInput, Textarea
from django.forms.utils import ErrorList

from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["lastname", "firstname", "afpa_number"]
        widgets = {
            'lastname': TextInput(attrs={'class': 'form-control'}),
            'firstname': TextInput(attrs={'class': 'form-control'}),
            'afpa_number': TextInput(attrs={'class': 'form-control'})
        }


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = ["mail", "phone_number", "afpa_card_img"]
        widgets = {
            'mail': TextInput(attrs={'class': 'form-control'}),
            'phone_number': TextInput(attrs={'class': 'form-control'}),
            'afpa_card_img': FileInput(attrs={'class': 'form-control'})
        }  

    def clean_mail(self):
        mail = self.cleaned_data['mail'].lower()
        r = PersonalData.objects.filter(mail=mail)
        if r.count():
            raise  forms.ValidationError("Email existe déjà")
        return mail


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street","street_number","street_complement"]
        widgets = {
            'street': TextInput(attrs={'class': 'form-control'}),
            'street_number': NumberInput(attrs={'class': 'form-control'}),
            'street_complement': TextInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        street_number = self.cleaned_data['street_number']
        street = self.cleaned_data['street']
        r = Address.objects.filter(street_number=street_number,street=street)
        if r.count():
            raise forms.ValidationError("l'adresse existe déjà")
        return cleaned_data


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


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('customer',)
        widgets = {
            'brand': TextInput(attrs={'class': 'form-control'}),
            'model': TextInput(attrs={'class': 'form-control'}),
            'license_plate': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'mileage': NumberInput(attrs={'class': 'form-control'}),
            'circulation_date': DateInput(attrs={'class': 'form-control', 'type':'date'}), 
            'grey_doc_img': FileInput(attrs={'class': 'form-control'}),
            'insurance_img': FileInput(attrs={'class': 'form-control'})
        }
       

class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        exclude = ('customer', 'grey_doc_img', 'insurance_img' )
        widgets = {
            'brand': TextInput(attrs={'class': 'form-control'}),
            'model': TextInput(attrs={'class': 'form-control'}),
            'license_plate': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'mileage': NumberInput(attrs={'class': 'form-control'}),
            'circulation_date': DateInput(attrs={'class': 'form-control'}),
            'grey_doc_img': FileInput(attrs={'class': 'form-control'}),
            'insurance_img': FileInput(attrs={'class': 'form-control'})
        }    
       

class ReparationOrderForm(forms.ModelForm):
    class Meta:
        model = ReparationOrder
        fields = ["committed_date","return_date","diagnostic","to_do_actions"]
        widgets = {
            'committed_date': DateInput(attrs={'class': 'form-control', 'type':'date'}),            
            'return_date': DateInput(attrs={'class': 'form-control', 'type':'date'}),    
            'diagnostic' : Textarea(attrs={'class': 'form-control'}),  
            'to_do_actions' : Textarea(attrs={'class': 'form-control'})
        }




