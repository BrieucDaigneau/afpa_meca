from django.http import HttpResponse
from .models import Client, DonneesPersonnelles, ZipCode, City, Voiture

from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import ClientForm, DonneesPersonnellesForm, AddressForm, ZipCodeForm, CityForm, VoitureForm
from django.views.generic import CreateView, ListView, View, FormView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Client, DonneesPersonnelles, Address, ZipCode, Voiture
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db import transaction


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
            with transaction.atomic():
                dico = self.getForm( request )
                    
                zipCode_form = dico['zipCode_form']
                if zipCode_form.is_valid():
                    zip_code = zipCode_form.cleaned_data['zip_code']
                    codepostal = ZipCode.objects.filter(zip_code=zip_code)
                    if not codepostal.exists():
                        zipCode = zipCode_form.save() 
                    else :
                        zipCode = codepostal[0]

                    city_form = dico['city_form']
                    if city_form.is_valid():
                        city_name = city_form.cleaned_data['city_name']   
                        ville = City.objects.filter(city_name=city_name)
                        if not ville.exists():
                            city = city_form.save() 
                        else :
                            city = ville[0]

                        city.zip_codes.add(zipCode)
                        city.save()

                        address_form = dico['address_form'] 
                        if address_form.is_valid():
                            address = address_form.save(commit=False)
                            address.zipCode = zipCode
                            address.city = city
                            address.save()

                            donneesPersonnelles_form = dico['donneesPersonnelles_form'] 
                            if donneesPersonnelles_form.is_valid():
                                donnees = donneesPersonnelles_form.save()    

                                client_form = dico['client_form'] 
                                if client_form.is_valid():
                                    client = client_form.save(commit=False)
                                    client.donnees_personnelles_client = donnees
                                    client.adresse = address
                                    client.save()
                                    dico = {
                            
                                        'client_id':client.id,
                                        'address_id':address.id,
                                        'zipCode_id':zipCode.id,
                                        'city_id':city.id,
                                        
    
                                    }
                                    return redirect("garage:ordre_reparation", **dico)

        except IntegrityError:
            client_form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
         
        return render(request, 'garage/client_form.html', self.getForm( request ) )
        # context['errors'] = client_form.errors.items()
        # return render(request, 'garage/client_form.html', context)


def ordre_reparation(request, client_id, address_id, zipCode_id, city_id):
    client = Client.objects.get(pk=client_id)
    donnees = DonneesPersonnelles.objects.get(pk=client_id)
    address = Address.objects.get(pk=address_id)
    zipCode = ZipCode.objects.get(pk=zipCode_id)
    city = City.objects.get(pk=city_id)
    
     
    context = {
        'donnees': donnees,
        'client': client,
        'address': address,    
        'zipCode': zipCode,
        'city': city,
       
    }
    
    # client = get_object_or_404(Client, id=id)
    return render(request, 'garage/ordre_reparation.html', context)    


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







class VoitureCreate(CreateView):
    model = Voiture
    fields = '__all__'
    def getForm(self, request):
        voiture_form = VoitureForm(request.POST or None)
        return {
            'voiture_form' : voiture_form
        
        }
    def get(self, request):
        myTemplate_name = 'garage/voiture_form.html'
        return render(request, myTemplate_name, self.getForm( request ) )