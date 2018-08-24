from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import CreateView, ListView, View, FormView, DetailView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError

from .models import *
from .forms import *
from . import urls


class Home(TemplateView):
    template_name = 'garage/home.html'

    # def get_context_data(self, **kwargs):
    #     context = super(Home, self).get_context_data(**kwargs)
    #     context['reparation_order_list'] = ReparationOrder.objects.filter(user_profile=self.request.user)
    #     return context


class CustomerCreateView(View):
    def getForm(self, request):
        zipCode_form = ZipCodeForm(request.POST or None)
        city_form = CityForm(request.POST or None)
        address_form = AddressForm(request.POST or None)    
        customer_form = CustomerForm(request.POST or None)   
        personal_data_form = PersonalDataForm(request.POST or None)

        return { 'customer_form': customer_form,
            'personal_data_form': personal_data_form,
            'address_form' : address_form,
            'city_form' : city_form,
            'zipCode_form' : zipCode_form
        }
    
    def get(self, request):
        myTemplate_name = 'garage/customer_form.html'
        return render(request, myTemplate_name, self.getForm( request ) )

    @transaction.atomic
    def post(self, request):
        try:
            modelFormError = ""
            with transaction.atomic():
                dictio = self.getForm( request )
                    
                zipCode_form = dictio['zipCode_form']
                if not zipCode_form.is_valid():
                    modelFormError = "Une erreur interne est apparue sur le code postal. Merci de recommencer votre saisie."                  
                    raise ValidationError(modelFormError)
                else :
                    try:
                        zip_code = zipCode_form.cleaned_data['zip_code']
                        current_zip_code = ZipCode.objects.filter(zip_code=zip_code)
                        if not current_zip_code.exists():
                            zipCode = zipCode_form.save() 
                        else :
                            zipCode = current_zip_code[0]

                    except DatabaseError:   
                        modelFormError = "Problème de connexion à la base de données 1"                  
                        raise                                


                    city_form = dictio['city_form']
                    if not city_form.is_valid():
                        modelFormError = "Une erreur interne est apparue sur la current_city. Merci de recommencer votre saisie."                  
                        raise ValidationError(modelFormError)
                    else :
                        try:
                            city_name = city_form.cleaned_data['city_name']   
                            current_city = City.objects.filter(city_name=city_name)
                            if not current_city.exists():
                                city = city_form.save() 
                            else :
                                city = current_city[0]

                            city.zip_codes.add(zipCode)
                            city.save()

                        except DatabaseError:   
                            modelFormError = "Problème de connexion à la base de données 2"                  
                            raise                                


                        address_form = dictio['address_form']                       
                        if not address_form.is_valid():                         
                            modelFormError = "Une erreur interne est apparue sur l'adresse. Merci de recommencer votre saisie."                  
                            raise ValidationError(modelFormError)
                        else :
                            try:
                                address = address_form.save(commit=False)
                                address.zipCode = zipCode
                                address.city = city
                                address.save()

                            except DatabaseError:   
                                modelFormError = "Problème de connexion à la base de données 3"                  
                                raise                                


                            personal_data_form = dictio['personal_data_form'] 
                            if not personal_data_form.is_valid():
                                modelFormError = "Une erreur interne est apparue sur les données personnelles. Merci de recommencer votre saisie."                  
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
                                        modelFormError = "Problème de connexion à la base de données 4"                  
                                        raise 
                                    
                                    return redirect("garage:vehicle-create", context['customer_id'])

        except (ValidationError, DatabaseError):
            dictioError = self.getForm( request )
            dictioError ['internal_error'] = modelFormError
            return render(request, 'garage/customer_form.html', dictioError )
         
        return render(request, 'garage/customer_form.html', self.getForm( request ) )


class CustomerSelect(ListView):
    model = Customer
    template_name = "garage/customer_select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer_list'] = self.get_queryset()
        return context


class CarCreate(CreateView):
    form_class = CarForm
    template_name = 'garage/car_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:reparation-order-create',
                                kwargs={'vehicle_id': self.object.id},
                                current_app='garage')

    def form_valid(self, form):
        customer = Customer.objects.get(pk=self.kwargs['customer_id'])
        car = form.save()
        car.customer = customer
        car.save()
        return super().form_valid(form)


class VehicleSelect(ListView):
    model = Car
    template_name = 'garage/car_select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_list'] = self.get_queryset()
        context['car_id'] = None
        return context
        
    def get_queryset(self):
        return Car.objects.filter(customer_id=self.kwargs['customer_id'])


class MotorbikeSelect(VehicleSelect):
    model = Motorbike

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_list'] = self.get_queryset()
        return context

    def get_queryset(self):
        return Motorbike.objects.filter(customer_id=self.kwargs['customer_id'])

    
class ReparationOrderCreate(CreateView):
    form_class = ReparationOrderForm
    template_name = 'garage/reparation_order.html'    

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:home',
                                current_app='garage')    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle = Vehicle.objects.filter_child(self.kwargs['vehicle_id'])       
        context['vehicle'] = vehicle   
        return context

    def form_valid(self, form):
        vehicle = Vehicle.objects.filter_child(self.kwargs['vehicle_id'])     
        user = self.request.user          
        reparation_order = form.save(commit=False)
        reparation_order.utilisateur = user
        reparation_order.vehicle = vehicle
        reparation_order.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get('query')
    if not query:
        customers = Customer.objects.all()
    else:
        # nom_client contains the query is and query is not sensitive to case.
        customers = Customer.objects.filter(lastname__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'context_object_name': customers
    }
    return render(request, 'garage/search.html', context) 


class VehicleList(VehicleSelect):
    template_name = 'garage/vehicles.html'


class VehiculeSelect(ListView):
    model = Vehicle
    template_name = 'garage/voiture-select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        context['voiture_id'] = None
        return context
        
    def get_queryset(self):
        # print(Vehicule.objects.get_child(self.kwargs['customer_id']))
        return Vehicule.objects.filter_child(self.kwargs['customer_id'])


class VehicleCreate(CreateView):
    template_name = 'garage/vehicle_form.html'

    def get_form_class(self) :
        if VehicleConfig['vehicle'] == 'car' :
            return CarForm    
        elif VehicleConfig['vehicle'] == 'bike' :
            return BikeForm   

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:reparation-order-create',
                                kwargs={'vehicle_id': self.object.id},
                                current_app='garage')

    def form_valid(self, form):
        customer = Customer.objects.get(pk=self.kwargs['customer_id'])

        # Attention vehicule est une instance de Voiture, Velo ou Moto
        vehicle = form.save()
        # print(Vehicule.objects.get_child(self.kwargs['customer_id']))        
        vehicle.customer = customer
        vehicle.save()
        return super().form_valid(form)        


