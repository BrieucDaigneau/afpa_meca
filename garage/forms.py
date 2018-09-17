from django import forms
from django.forms import ModelForm, TextInput, EmailInput, SelectDateWidget, FileInput, NumberInput, DateInput, Textarea, NumberInput, Select
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

class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street","street_number","street_complement"]
        widgets = {
            'street': TextInput(attrs={'class': 'form-control'}),
            'street_number': NumberInput(attrs={'class': 'form-control'}),
            'street_complement': TextInput(attrs={'class': 'form-control'})
        }


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


class ComponentForm(forms.Form):
    
    reference = forms.CharField()
    name = forms.CharField()
    price = forms.FloatField()
    quantity = forms.IntegerField()
    
    reference.widget.attrs.update({'class': 'form-control'})
    name.widget.attrs.update({'class': 'form-control'})
    price.widget.attrs.update({'class': 'form-control'})
    quantity.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()

    def save(self):
        data = self.clean()
        component = Component(reference=data['reference'], name=data['name'], price=data['price'], supplier=quotation.supplier)
        component.save()
        quotation_line = QuotationLine(quantity=data['quantity'], component=component, quotation=quotation)
        quotation_line.save()

class QuotationForm(forms.Form):
    number = forms.CharField()
    amount = forms.FloatField()
    signed_img = forms.FileField()
    payoff_date = forms.DateField()
    payoff_type = forms.ChoiceField()
    name = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=Select(attrs={'class': 'custom-select'}))
                                            
    num_quotation_supplier = forms.CharField()
        
    number.widget.attrs.update({'class': 'form-control'})
    amount.widget.attrs.update({'class': 'form-control'})
    signed_img.widget.attrs.update({'class': 'form-control'})
    payoff_date.widget.attrs.update({'class': 'form-control'})
    payoff_type.widget.attrs.update({'class': 'form-control'})
    num_quotation_supplier.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data
        quotation_id_max = list(Quotation.objects.all().aggregate(Max('id')).values())[0]
        number = quotation_id_max + 1 if quotation_id_max is not None else 0

        supplier = Supplier(name=data['name'])
        
        quotation = Quotation(number=number, supplier=supplier,
                             num_quotation_supplier=data['num_quotation_supplier'], 
                             user_profile=self.request.user, 
                             reparation_order=self.kwargs['reparation_order_id'],
                             amount=0.00)
        quotation.save()
        return quotation

    def save(self):
        pass


# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = "__all__"
#         widgets = {
#             'name': TextInput(attrs={'class': 'form-control'}),
#             'num_quotation_supplier': TextInput(attrs={'class': 'form-control'}),
#         }

# class ComponentForm(forms.ModelForm):
#     class Meta:
#         model = Component
#         exclude = ('supplier',)
#         widgets = {
#             'reference': TextInput(attrs={'class': 'form-control'}),
#             'name': TextInput(attrs={'class': 'form-control'}),
#             'price': NumberInput(attrs={'class': 'form-control'}),

#         }

# class QuantityForm(forms.ModelForm):
#     class Meta:
#         model = Quantity
#         fields = "__all__"
#         widgets = {
#             'quantity': NumberInput(attrs={'class': 'form-control'}),
#         }


        # fields =['signed_img', 'payoff_date', 'payoff_type']
    # quantity     = models.IntegerField("quantité pièce", max_length=3)
    # number       = models.CharField(unique=True, max_length=15)
    # date         = models.DateField("Date du devis", null=False, default=datetime.now)
    # signed_img   = models.ImageField("Scan du devis signé", null=True, upload_to ="img/devis")
    # amount       = models.FloatField("Total TTC")