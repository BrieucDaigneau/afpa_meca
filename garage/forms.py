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

class AddressForm(forms.ModelForm):  
    class Meta:
        model = Address
        fields = ["city","zip_code",]
        widgets = {
            'city': TextInput(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            
        }

    city_zip_code = forms.CharField(widget=TextInput(attrs={'class': 'form-control require-input', 
                                                        'v-model': 'cityZipCode', 'autocomplete': 'off'}),
                                label="Ville ou Code Postal", required=True)

    address = forms.CharField(widget=TextInput(attrs={'class': 'form-control require-input', 
                                                        'v-model': 'address', 'autocomplete': 'off'}),
                        label="Adresse", required=True)

    json_hidden = forms.CharField(widget=forms.HiddenInput(attrs={'v-model': 'addressJSON'}))

    def clean(self):
        json = self.cleaned_data.get('json_hidden')
        if not json:
            raise forms.ValidationError("Veuillez sélectionner une adresse")
        return self.cleaned_data


class AddressUpdateForm(forms.ModelForm):
     class Meta:
        model = Address
        fields = ["city", "zip_code", "street_number","street_name"]
        widgets = {
            'city': TextInput(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            'street_number': TextInput(attrs={'class': 'form-control'}),
            'street_name': TextInput(attrs={'class': 'form-control'}),
        }
        


class MotorizedForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('customer',)
        widgets = {
            'brand': TextInput(attrs={'class': 'form-control'}),
            'model_name': TextInput(attrs={'class': 'form-control'}),
            'license_plate': TextInput(attrs={'class': 'form-control'}),
            'vin': TextInput(attrs={'class': 'form-control'}),
            'mileage': NumberInput(attrs={'class': 'form-control'}),
            'circulation_date': DateInput(attrs={'class': 'form-control', 'type':'date'}), 
            'grey_doc_img': FileInput(attrs={'class': 'form-control'}),
            'insurance_img': FileInput(attrs={'class': 'form-control'})
        }

       
class CarForm(MotorizedForm):
    class Meta(MotorizedForm.Meta) :
        model = Car
 

class MotorbikeForm(MotorizedForm):
    class Meta(MotorizedForm.Meta) :
        model = Motorbike
 
 
class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['model_name']
        widgets = {
            'model_name': TextInput(attrs={'class': 'form-control'}),
        }
       

class ReparationOrderForm(forms.ModelForm):
    class Meta:
        model = ReparationOrder
        fields = ["return_date","diagnostic","to_do_actions"]
        widgets = {
            'return_date': DateInput(attrs={'class': 'form-control','type':'date'}),    
            'diagnostic' : Textarea(attrs={'class': 'form-control'}),  
            'to_do_actions' : Textarea(attrs={'class': 'form-control'})
        }




