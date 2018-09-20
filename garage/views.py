from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse, render_to_response
from django.views.generic import CreateView, ListView, View, FormView, DetailView, TemplateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError
from django.db.models import Max, Sum

import json

from .models import *
from .forms import *
from . import urls
from afpa_meca.business_application import VehicleConfig

class Home(TemplateView):
    template_name = 'garage/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['reparation_order_list'] = ReparationOrder.objects.filter(user_profile=self.request.user)
        return context


class CustomerCreateView(View):

    def getForm(self, request):
        address_form = AddressForm(request.POST or None)    
        customer_form = CustomerForm(request.POST or None)   
        personal_data_form = PersonalDataForm(request.POST, request.FILES)

        return { 'customer_form': customer_form,
            'personal_data_form': personal_data_form,
            'address_form' : address_form,
        }
    
    def get(self, request):
        template_name = 'garage/customer_form.html'
        return render(request, template_name, self.getForm( request ) )

    @transaction.atomic
    def post(self, request):
        try:
            modelFormError = ""
            with transaction.atomic():
                dictio = self.getForm( request )   

                address_form = dictio['address_form']
                print("erreur 3", address_form)
                                     
                if not address_form.is_valid():                         
                    modelFormError = "Une erreur interne est apparue sur l'adresse. Merci de recommencer votre saisie."                  
                    raise ValidationError(modelFormError)
                else :
                    try:
                        address = address_form.save(commit=False)
                        print("erreur 1")
                        json_data = json.loads(address_form.cleaned_data['json_hidden'])
                        prop = json_data['properties']
                        address.city = prop['city']
                        address.zip_code = prop['postcode']
                        street = prop.get('street')
                        street_number = prop.get('housenumber')
                        name = prop.get('name')
                        if street and street_number:
                            address.street_number = street_number
                            address.street_name = street
                        else:
                            address.street_name = name
                        print("erreur 2")
                        address.save()
                    
                    except DatabaseError:   
                        modelFormError = "Problème de connexion à la base de données"                  
                        raise                                

                    personal_data_form = dictio['personal_data_form'] 
                    if not personal_data_form.is_valid():
                        modelFormError = "Un objet Donnée Personnelle avec ce champ Email existe déjà."
                        raise ValidationError(modelFormError)
                    else :
                        data = personal_data_form.save()    

                        customer_form = dictio['customer_form'] 
                        if not customer_form.is_valid():
                            modelFormError = "Une erreur interne est apparue sur les données clients. Merci de recommencer votre saisie."                  
                            raise ValidationError(modelFormError)
                        else :
                            try:
                                customer = customer_form.save(commit=False)
                                customer.personal_data = data
                                customer.address = address
                                customer.save()   
                                context = {'customer_id':customer.id}

                            except DatabaseError:   
                                modelFormError = "Problème de connexion à la base de données"                  
                                raise 
                            
                            return redirect("garage:vehicle-create", context['customer_id'])

        except (ValidationError, DatabaseError):
            dictioError = self.getForm( request )
            dictioError ['internal_error'] = modelFormError
            return render(request, 'garage/customer_form.html', dictioError )
         
        return render(request, 'garage/customer_form.html', self.getForm( request ) )

class CustomerUpdate(UpdateView):
    template_name = 'garage/customer_update.html'
    success_message = "Données mises à jour avec succès"

    def my_get_form(self, param):
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        address = customer.address
        personalData = customer.personal_data

        address_Form = AddressUpdateForm(param, instance=address)
        personnalData_Form = PersonalDataForm(param, instance=personalData)
        customer_Form = CustomerForm(param, instance=customer)
    
        return {
                'address_form': address_Form, 'personal_data_form': personnalData_Form,
                'customer_form': customer_Form,}

    def get(self, request, **kwargs):       
        return render(request, self.template_name, self.my_get_form(None))

    def post (self, request, **kwargs):
        dico = self.my_get_form(request.POST)
        
        address_Form = dico['address_form']
        personnalData_Form = dico['personal_data_form']
        customer_Form = dico['customer_form']

        if address_Form.is_valid() and personnalData_Form.is_valid() and customer_Form.is_valid():     
            addressData = address_Form.save(commit=False)
            personalDataData = personnalData_Form.save(commit=False)
            customerData = customer_Form.save(commit=False)
            
            addressData.save()
            customerData.address = addressData

            personalDataData.save()
            customerData.personal_data = personalDataData

            customerData.save()
            
            return redirect('garage:customers')

        context = {
            'address_form': address_Form, 'personal_data_form': personnalData_Form, 'customer_form': customer_Form,}
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        customer = Customer.objects.filter(pk=self.kwargs['pk'])
        address = customer.address
        personalData = customer.personal_data
        context = super(CustomerUpdate, self).get_context_data(**kwargs)

        if 'address_form' not in context:
            context['address_form'] = AddressUpdateForm(instance=address)
        if 'personal_data_form' not in context:
            context['personal_data_form'] = PersonalDataForm(instance=personalData)
        if 'personal_data_form' not in context:
            context['personal_data_form'] = CustomerForm(instance=customer)
        return context 


class CustomerSelect(ListView):
    model = Customer
    template_name = "garage/customer_select.html"


class Customers(CustomerSelect):
    template_name = "garage/customers.html"


class VehicleCreate(View):
    template_name = 'garage/vehicle_form.html'

    def getForm(self, request ) :
        dico = {}

        if VehicleConfig['vehicle'] == 'car' :
            dico = {
                "form": CarForm(request.POST, request.FILES),
                "vehicle_type": "motorised",
                "bike_form": "None"
            }
        elif VehicleConfig['vehicle'] == 'bike' :
            dico = {
                "form": MotorbikeForm(request.POST, request.FILES),
                "bike_form": BikeForm(request.POST),
                "vehicle_type": "twowheelers"
            }
        return dico  

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.getForm( request ) )

    def post(self, request, **kwargs):
        forms = self.getForm(request)

        if forms['form'].is_valid():
            form = forms['form']
        elif forms['bike_form'] != "None" and forms['bike_form'].is_valid():
            form = forms['bike_form']
        else:
            return render( request, self.template_name, self.getForm( request ))  

        customer = Customer.objects.get(pk=self.kwargs['customer_id'])

        vehicle = form.save(commit=False)
        vehicle.customer = customer
        vehicle.save()
        return redirect("garage:reparation-order-create", vehicle.id)  


class VehicleSelect(ListView):
    model = Vehicle
    template_name = "garage/vehicle_select.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_list'] = Vehicle.objects.filter_by_user(self.kwargs['customer_id'])
        return context  


class Vehicles(ListView):
    model = Vehicle
    template_name = "garage/vehicles.html"    

    def get_context_data(self, **kwargs):    
        context = super().get_context_data(**kwargs)   
        vehicles = [Vehicle.objects.get_child(v.id) for v in Vehicle.objects.all()]
        context['vehicle_list'] = Vehicle.objects.filter_type(vehicles)
        return context  


class VehicleUpdate(UpdateView):
    template_name = 'garage/vehicle_update.html'
    success_url = reverse_lazy('garage:vehicles')

    def get_form_class(self) :
        v = self.get_object()

        if isinstance(v, Car) :
            return CarForm   
        if isinstance(v, Motorbike) :
            return MotorbikeForm             
        if isinstance(v, Bike) :
            return BikeForm

    def get_object(self):
        return Vehicle.objects.get_child(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reparation_order_list'] = ReparationOrder.objects.filter(vehicle=self.kwargs['pk'])
        context['vehicle_type'] = "bike" if self.get_form_class() == BikeForm else "motorised"
        return context


class ReparationOrderCreateView(CreateView):
    form_class = ReparationOrderForm
    template_name = 'garage/reparation_order.html'    

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:home', current_app='garage')    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reparations_orders = ReparationOrder.objects.filter(vehicle=self.kwargs['vehicle_id'])
        context['reparations_orders'] = reparations_orders
        if reparations_orders:
            context['nb_AF'] = len(reparations_orders.filter(status="AttenteFormateur"))
            context['nb_VF'] = len(reparations_orders.filter(status="ValidationFormateur"))
            context['nb_RF'] = len(reparations_orders.filter(status="RefusFormateur"))
            context['nb_AD'] = len(reparations_orders.filter(status="AttenteDevis"))

        vehicle = Vehicle.objects.get_child(self.kwargs['vehicle_id'])  
        context['vehicle'] = vehicle   
        return context

    def form_valid(self, form):
        vehicle = Vehicle.objects.get(pk=self.kwargs['vehicle_id'])     
        user = self.request.user          
        reparation_order = form.save(commit=False)
        reparation_order.user_profile = user
        reparation_order.vehicle = vehicle
        reparation_order.save()
        return super().form_valid(form)        


class ReparationOrderSelect(ListView):
    model = ReparationOrder
    template_name = "garage/reparation_orders_select.html"


class ReparationOrders(ReparationOrderSelect):
    template_name = "garage/reparation_orders.html"
    

class ReparationOrderUpdate(UpdateView):
    template_name = 'garage/reparation_order_update.html'   
    success_url = reverse_lazy('garage:reparation-orders')
    # remarque : le projet plante sans le model et form_class 
    model = ReparationOrder
    form_class = ReparationOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reparationorder = ReparationOrder.objects.get(pk=self.kwargs['pk'])  
        context['reparationorder'] = reparationorder
        context['vehicle'] =  reparationorder.vehicle
        return context  


def car_condition(request):
    return render(request, 'garage/car_condition.html')


def search(request):
    query = request.GET.get('query')
    if not query:
        customers = Customer.objects.all()
    else:
        customers = Customer.objects.filter(lastname__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'context_object_name': customers
    }
    return render(request, 'garage/search.html', context) 


class QuotationCreate(View): 
    myTemplate_name = 'garage/quotation_create.html'

    def getForm(self, requ):
        quotation_form = QuotationForm(requ)
        component_form = ComponentForm(requ)

        dico = {
            'quotation_form': quotation_form,
            'component_form': component_form,

        }
        return dico
    
    def get(self, request, **kwargs):
        return render(request, self.myTemplate_name, self.getForm( None ) )
    
    def post(self, request, **kwargs):
        forms = self.getForm(request.POST)

        quotation_form = forms['quotation_form']
        component_form = forms['component_form']

        print( "####" , quotation_form )
        
        if component_form.is_valid() and quotation_form.is_valid() :
            
            quotation = quotation_form.save(commit=False)
            
            # attribution d'un id de devis
            quotation_id_max = list(Quotation.objects.all().aggregate(Max('id')).values())[0]
            quotation.number = quotation_id_max + 1 if quotation_id_max is not None else 0   


            quotation.reparation_order = ReparationOrder.objects.get(pk=self.kwargs['reparation_orders_id'])
            quotation.user_profile = self.request.user

            quotation.amount = 0 #component.price*component.quantity
            quotation.save()

            component = Component.objects.create(price=component_form.cleaned_data['price'],
                                                reference=component_form.cleaned_data['reference'],
                                                name=component_form.cleaned_data['name'],
                                                quantity=component_form.cleaned_data['quantity'],
                                                supplier=quotation.supplier,
                                                quotation=quotation)

            component.save()

            return redirect('garage:home')
            
        else : 
            print( "################# quotation_form invalid")
            return render(request, 'garage/quotation_create.html')

    def get_context_data(self, **kwargs):
        context = super(QuotationCreate, self).get_context_data(**kwargs)
        context['reparation_order'] = ReparationOrder.object.get(pk=self.kwargs['reparation_orders_id'])
        print("#######################", context)
        return context