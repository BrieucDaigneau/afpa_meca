from django import forms
from django.forms import ModelForm, TextInput, EmailInput, SelectDateWidget, FileInput, NumberInput, DateInput, Textarea, NumberInput, Select, formset_factory, modelformset_factory, DateTimeInput
from django.forms.utils import ErrorList
from django.db.models import Max

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
        fields = ["street_complement"]
        widgets = {
            'street_complement': TextInput(attrs={'class': 'form-control'}),    
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
        fields = ["city", "zip_code", "street_number","street_name", "street_complement"]
        widgets = {
            'city': TextInput(attrs={'class': 'form-control'}),
            'zip_code': TextInput(attrs={'class': 'form-control'}),
            'street_number': TextInput(attrs={'class': 'form-control'}),
            'street_name': TextInput(attrs={'class': 'form-control'}),
            'street_complement': TextInput(attrs={'class': 'form-control'}),
        }
        


class MotorizedForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ('customer',)
        widgets = {
            'brand': TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'model_name': TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'license_plate': TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'vin': TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'mileage': NumberInput(attrs={'class': 'form-control'}),
            'circulation_date': DateInput(attrs={'class': 'form-control', 'type':'date', 'required':'true'}), 
            'grey_doc_img': FileInput(attrs={'class': 'form-control', 'required':'true'}),
            'insurance_img': FileInput(attrs={'class': 'form-control', 'required':'true'})
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
            'model_name': TextInput(attrs={'class': 'form-control', 'required':'True'}),
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


class ComponentForm(forms.ModelForm):
    def __init__(self, *arg, **kwarg):
        super(ComponentForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = False

    class Meta:
        model = Component
        exclude = ("supplier", "quotation")
        widgets = {
            'quantity': NumberInput(attrs={'value':'1', 'class': 'form-control col-md-1 quantity', 'required':'True', 'onchange':'majTotal()'}),
            'reference': TextInput(attrs={'class': 'form-control col-md-4', 'required':'True'}),
            'name': TextInput(attrs={'class': 'form-control col-md-4', 'required':'True'}),
            'price':NumberInput(attrs={'class': 'form-control col-md-2', 'required':'True', 'onchange':'majTotal()'})
        }
    # quantity = forms.IntegerField(required=True, min_value=1)
    # reference = forms.CharField(required=True)
    # name = forms.CharField(required=True)
    # price = forms.FloatField(required=True, min_value=0)
    
    # quantity.widget.attrs.update({'class': 'form-control col-md-1'})
    # reference.widget.attrs.update({'class': 'form-control col-md-4'})
    # name.widget.attrs.update({'class': 'form-control col-md-4'})
    # price.widget.attrs.update({'class': 'form-control col-md-2'})
    
    # def formset_factory(self, form, formset=ComponentFormSet, extra=2):
    #     formset = ComponentFormSet()

ComponentFormset = formset_factory(ComponentForm)
ComponentModelFormset = modelformset_factory(Component, 
                                        exclude = ("supplier", "quotation"),
                                        widgets = {
                                                    'quantity': NumberInput(attrs={'value':'1', 'class': 'form-control col-md-1 quantity', 'required':'True', 'onchange':'majTotal()'}),
                                                    'reference': TextInput(attrs={'class': 'form-control col-md-4', 'required':'True'}),
                                                    'name': TextInput(attrs={'class': 'form-control col-md-4', 'required':'True'}),
                                                    'price':NumberInput(attrs={'class': 'form-control col-md-2', 'required':'True', 'onchange':'majTotal()'})
                                                },
                                        extra = 0 
                                        )

class QuotationForm(forms.ModelForm):

    supplier = forms.ModelChoiceField(queryset=None, widget=Select(attrs={'class': 'custom-select'}), 
                                            label="Départ" )                                                    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter()

    class Meta:
        model = Quotation
        fields =('supplier', 'num_quotation_supplier', 'amount')
        widgets = {
            'num_quotation_supplier' : TextInput(attrs={'class': 'form-control'}),
            'amount' : NumberInput(attrs={'class': 'form-control'}),
        }
class QuotationUpdateForm(QuotationForm):
                                  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payoff_type'].queryset = Quotation.payoff_choice

    class Meta:
        model = Quotation
        fields =('supplier', 'num_quotation_supplier', 'amount', 'payoff_type', 'payoff_date')
        widgets = {
            'num_quotation_supplier' : TextInput(attrs={'class': 'form-control'}),
            'amount' : NumberInput(attrs={'class': 'form-control'}),
            'payoff_type': Select(attrs={'class': 'form-control', 'onchange':'auto_payoff_date()'}),
            'payoff_date': DateTimeInput(attrs={'class': 'form-control', 'type':'date', 'required':'true', 'value':''})

        }
    

# ComponentFormSet = formset_factory(ComponentForm, extra=2)
# formset = ComponentFormSet