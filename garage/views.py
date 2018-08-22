from django.http import HttpResponse
from .models import *

from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import ClientForm, DonneesPersonnellesForm, AddressForm, ZipCodeForm, CityForm, VoitureForm, InterventionForm
from django.views.generic import CreateView, ListView, View, FormView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from . import urls

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError

class Home(TemplateView):
    template_name = 'garage/home.html')

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['reparation_order_list'] = ReparationOrder.objects.filter(user_profile=self.request.user)
        return context


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
                        modelFormError = "Problème de connexion à la base de données"                  
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
                            modelFormError = "Problème de connexion à la base de données"                  
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
                                modelFormError = "Problème de connexion à la base de données"                  
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
                                        customer.personal_data_form = data
                                        customer.address = address
                                        customer.save()                        
                                        context = {'customer_id':customer.id}

                                    except DatabaseError:   
                                        modelFormError = "Problème de connexion à la base de données"                  
                                        raise 
                                    
                                    return redirect("garage:car-create", context['customer_id'])

        except (ValidationError, DatabaseError):
            dictioError = self.getForm( request )
            dictioError ['internal_error'] = modelFormError
            return render(request, 'garage/customer_form.html', dictioError )
         
        return render(request, 'garage/customer_form.html', self.getForm( request ) )

class ClientSelect(ListView):
    model = Client
    template_name = "garage/client-select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['liste_client'] = self.get_queryset()
        # print(context)
        return context


class VoitureCreate(CreateView):
    form_class = VoitureForm
    template_name = 'garage/voiture_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:intervention-create',
                                kwargs={'vehicule_id': self.object.id},
                                current_app='garage')

    def form_valid(self, form):
        client = Client.objects.get(pk=self.kwargs['client_id'])
        voiture = form.save()
        voiture.client = client
        voiture.save()
        return super().form_valid(form)


class VehiculeSelect(ListView):
    model = Voiture
    template_name = 'garage/voiture-select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        context['voiture_id'] = None
        return context
        
    def get_queryset(self):
        return Voiture.objects.filter(client_id=self.kwargs['client_id'])


class MotoSelect(VehiculeSelect):
    model = Moto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        return context

    def get_queryset(self):
        return Moto.objects.filter(client_id=self.kwargs['client_id'])

    


class Intervention(CreateView):
    form_class = InterventionForm
    template_name = 'garage/intervention.html'    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicule = Vehicule.objects.get(pk=self.kwargs['vehicule_id'])
        context['vehicule'] = vehicule   
        return context

    def form_valid(self, form):
        vehicule = Vehicule.objects.get(pk=self.kwargs['vehicule_id'])
        intervention = form.save()
        intervention.vehicule = vehicule
        intervention.save()
        return super().form_valid(form)


def recherche(request):
    query = request.GET.get('query')
    if not query:
        clients = Client.objects.all()
    else:
        # nom_client contains the query is and query is not sensitive to case.
        clients = Client.objects.filter(nom_client__icontains=query)
    title = "Résultats pour la requête %s"%query
    context = {
        'context_object_name': clients
    }
    return render(request, 'garage/recherche.html', context) 

class VehiculeList(VehiculeSelect):
    template_name = 'garage/vehicules.html'

   
def ChoixVehicule(request):
    pass

