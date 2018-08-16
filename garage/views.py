from django.http import HttpResponse
from .models import *

from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import ClientForm, DonneesPersonnellesForm, AddressForm, ZipCodeForm, CityForm, VoitureForm, InterventionForm, MotoForm, VeloForm
from django.views.generic import CreateView, UpdateView, ListView, View, FormView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from . import urls

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db import DatabaseError, transaction
from django.core.exceptions import ValidationError


def accueil(request):
    return render(request, 'garage/accueil.html')


class ClientCreateView(View):
    def getForm(self, request):
        zipCode_form = ZipCodeForm(request.POST or None)
        city_form = CityForm(request.POST or None)
        address_form = AddressForm(request.POST or None)    
        client_form = ClientForm(request.POST or None)   
        donneesPersonnelles_form = DonneesPersonnellesForm(request.POST or None)

        return { 'client_form': client_form,
            'donneesPersonnelles_form': donneesPersonnelles_form,
            'address_form' : address_form,
            'city_form' : city_form,
            'zipCode_form' : zipCode_form
        }
    
    def get(self, request):
        myTemplate_name = 'garage/client_form.html'
        return render(request, myTemplate_name, self.getForm( request ) )

    @transaction.atomic
    def post(self, request):
        try:
            modelFormError = ""
            with transaction.atomic():
                dico = self.getForm( request )
                    
                zipCode_form = dico['zipCode_form']
                if not zipCode_form.is_valid():
                    modelFormError = "Une erreur interne est apparue sur le code postal. Merci de recommencer votre saisie."                  
                    raise ValidationError(modelFormError)
                else :
                    try:
                        zip_code = zipCode_form.cleaned_data['zip_code']
                        codepostal = ZipCode.objects.filter(zip_code=zip_code)
                        if not codepostal.exists():
                            zipCode = zipCode_form.save() 
                        else :
                            zipCode = codepostal[0]

                    except DatabaseError:   
                        modelFormError = "Problème de connection à la base de données"                  
                        raise                                


                    city_form = dico['city_form']
                    if not city_form.is_valid():
                        modelFormError = "Une erreur interne est apparue sur la ville. Merci de recommencer votre saisie."                  
                        raise ValidationError(modelFormError)
                    else :
                        try:
                            city_name = city_form.cleaned_data['city_name']   
                            ville = City.objects.filter(city_name=city_name)
                            if not ville.exists():
                                city = city_form.save() 
                            else :
                                city = ville[0]

                            city.zip_codes.add(zipCode)
                            city.save()

                        except DatabaseError:   
                            modelFormError = "Problème de connection à la base de données"                  
                            raise                                


                        address_form = dico['address_form']                       
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
                                modelFormError = "Problème de connection à la base de données"                  
                                raise                                


                            donneesPersonnelles_form = dico['donneesPersonnelles_form'] 
                            if not donneesPersonnelles_form.is_valid():
                                modelFormError = "Une erreur interne est apparue sur les données personnelles. Merci de recommencer votre saisie."                  
                                raise ValidationError(modelFormError)
                            else :
                                donnees = donneesPersonnelles_form.save()    


                                client_form = dico['client_form'] 
                                if not client_form.is_valid():
                                    modelFormError = "Une erreur interne est apparue sur les données clients. Merci de recommencer votre saisie."                  
                                    raise ValidationError(modelFormError)
                                else :
                                    try:
                                        client = client_form.save(commit=False)
                                        client.donnees_personnelles_client = donnees
                                        client.adresse = address
                                        client.save()                        
                                        context = {'client_id':client.id}

                                    except DatabaseError:   
                                        modelFormError = "Problème de connection à la base de données"                  
                                        raise 
                                    
                                    return redirect("garage:voiture-create", context['client_id'])

        except (ValidationError, DatabaseError):
            dicoError = self.getForm( request )
            dicoError ['internal_error'] = modelFormError
            return render(request, 'garage/client_form.html', dicoError )
         
        return render(request, 'garage/client_form.html', self.getForm( request ) )

class ClientSelect(ListView):
    model = Client
    template_name = "garage/client-select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_client'] = self.get_queryset()
        return context

class Clients(ClientSelect):
    template_name = "garage/clients.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        voiture.type_vehicule = "Voiture"
        voiture.save()
        return super().form_valid(form)


class MotoCreate(CreateView):
    form_class = MotoForm
    template_name = 'garage/moto_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:intervention-create',
                                kwargs={'vehicule_id': self.object.id},
                                current_app='garage')

    def form_valid(self, form):
        client = Client.objects.get(pk=self.kwargs['client_id'])
        moto = form.save()
        moto.type_vehicule = "Moto"
        moto.client = client
        moto.save()
        return super().form_valid(form)

class VeloCreate(CreateView):
    form_class = VeloForm
    template_name = 'garage/velo_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('garage:intervention-create',
                                kwargs={'vehicule_id': self.object.id},
                                current_app='garage')

    def form_valid(self, form):
        client = Client.objects.get(pk=self.kwargs['client_id'])
        velo = form.save()
        velo.type_vehicule = "Velo"
        velo.client = client
        velo.save()
        return super().form_valid(form)


class VoitureUpdate(UpdateView):
    model = Voiture
    template_name = 'garage/voiture_form.html'
    form_class = VoitureForm
    success_url = reverse_lazy('garage:voitures')

class MotoUpdate(UpdateView):
    model = Moto
    template_name = 'garage/voiture_form.html'
    form_class = MotoForm
    success_url = reverse_lazy('garage:voitures')

class VeloUpdate(UpdateView):
    model = Velo
    template_name = 'garage/velo_form.html'
    form_class = VeloForm
    success_url = reverse_lazy('garage:')


class VehiculeSelect(ListView):
    model = Voiture
    template_name = 'garage/voiture-select.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        context['voiture_id'] = None
        context['curent_model'] = "Voiture"
        if self.template_name == 'garage/voiture-select.html':
            client = Client.objects.get(pk=self.kwargs['client_id'])
            context['client'] = client
        return context
        
    def get_queryset(self):
        return Voiture.objects.filter(client_id=self.kwargs['client_id'])

class MotoSelect(VehiculeSelect):
    model = Moto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        context['curent_model'] = "Moto"
        print("############################################################", context)
        return context

    def get_queryset(self):
        return Moto.objects.filter(client_id=self.kwargs['client_id'])

class VeloSelect(VehiculeSelect):
    model = Velo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_vehicule'] = self.get_queryset()
        context['curent_model'] = "Velo"
        return context

    def get_queryset(self):
        return Velo.objects.filter(client_id=self.kwargs['client_id'])


class VehiculeList(VehiculeSelect):
    template_name = 'garage/vehicules.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curent_model'] = "Voiture"
        return context
        
    def get_queryset(self):
        return Voiture.objects.all()

class MotoList(VehiculeSelect):
    template_name = 'garage/vehicules.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curent_model'] = "Moto"
        return context
        
    def get_queryset(self):
        return Moto.objects.all()

class VeloList(VehiculeSelect):
    template_name = 'garage/vehicules.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curent_model'] = "Velo"
        return context
        
    def get_queryset(self):
        return Velo.objects.all()


class InterventionCreate(CreateView):
    form_class = InterventionForm
    template_name = 'garage/ordre_reparation.html'    
    def get_success_url(self, **kwargs):

        return reverse_lazy('garage:accueil',
                                current_app='garage')

    def form_valid(self, form):
        vehicule = Voiture.objects.get(pk=self.kwargs['vehicule_id'])
        user = self.request.user

        intervention = form.save(commit=False)
        intervention.utilisateur = user
        intervention.vehicule = vehicule

        intervention.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Vehicule.objects.get(pk=self.kwargs['vehicule_id']).type_vehicule == "Voiture":
            vehicule = Voiture.objects.get(pk=self.kwargs['vehicule_id'])

        elif Vehicule.objects.get(pk=self.kwargs['vehicule_id']).type_vehicule == "Moto":
            vehicule = Moto.objects.get(pk=self.kwargs['vehicule_id'])

        elif Vehicule.objects.get(pk=self.kwargs['vehicule_id']).type_vehicule == "Velo":
            vehicule = Velo.objects.get(pk=self.kwargs['vehicule_id'])

        context['vehicule'] = vehicule   
        return context

class InterventionSelect(ListView):
    model = Intervention
    template_name = "garage/intervention-select.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liste_interventions'] = self.get_queryset()
        return context

class Interventions(InterventionSelect):
    template_name = "garage/interventions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class InterventionUpdate(UpdateView):
    model = Intervention
    form_class = InterventionForm
    template_name = 'garage/ordre_reparation.html'   
    success_url = reverse_lazy('garage:interventions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        intervention = Intervention.objects.get(pk=self.kwargs['pk'])
        if intervention.vehicule.type_vehicule == "Voiture":
            vehicule = Voiture.objects.get(pk=intervention.vehicule)

        elif intervention.vehicule.type_vehicule == "Moto":
            vehicule = Moto.objects.get(pk=intervention.vehicule)

        elif intervention.vehicule.type_vehicule == "Velo":
            vehicule = Velo.objects.get(pk=intervention.vehicule)

        context['vehicule'] = vehicule   
        return context  

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


   
def ChoixVehicule(request):
    pass

