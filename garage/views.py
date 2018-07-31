from django.http import HttpResponse
from .models import Client, DonneesPersonnelles, ZipCode, City

from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import ClientForm, DonneesPersonnellesForm, AddressForm, ZipCodeForm, CityForm
from django.views.generic import CreateView, ListView, View, FormView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Client, DonneesPersonnelles, Address, Motorise
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


def accueil(request):
    return render(request, 'garage/accueil.html')

class ClientCreateView(View):

    def post(self, request):
        pass


def clientCreate(request):
    sauvegarde = False
    zipCode_form = ZipCodeForm(request.POST or None)
    city_form = CityForm(request.POST or None)
    address_form = AddressForm(request.POST or None)    
    client_form = ClientForm(request.POST or None)   
    donneesPersonnelles_form = DonneesPersonnellesForm(request.POST or None)

    zipCode_form = ZipCodeForm(request.POST or None)
    if zipCode_form.is_valid():
        zip_code = zipCode_form.cleaned_data['zip_code']
        codepostal = ZipCode.objects.filter(zip_code=zip_code)
        if not codepostal.exists():
            zipCode = zipCode_form.save() 
        else :
            zipCode = codepostal[0]

        city_form = CityForm(request.POST or None)
        if city_form.is_valid():
            city_name = city_form.cleaned_data['city_name']   
            ville = City.objects.filter(city_name=city_name)
            if not ville.exists():
                city = city_form.save() 
            else :
                city = ville[0]

            city.zip_codes.add(zipCode)
            city.save()

            address_form = AddressForm(request.POST or None)    
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.zipCode = zipCode
                address.city = city
                address.save()

                donneesPersonnelles_form = DonneesPersonnellesForm(request.POST or None)
                if donneesPersonnelles_form.is_valid():
                    donnees = donneesPersonnelles_form.save()    

                    client_form = ClientForm(request.POST or None) 
                    if client_form.is_valid():
                        client = client_form.save(commit=False)
                        client.donnees_personnelles_client = donnees
                        client.adresse = address
                        client.save()                        
                        sauvegarde = True
                        dico = {
                            
                            'client_id':client.id,
                            'address_id':address.id,
                            'zipCode_id':zipCode.id,
                            'city_id':city.id,
    
                            }


                        return redirect("garage:ordre_reparation", **dico)
                

    return render(
        request, 
        'garage/client_form.html', 
        {   'client_form': client_form,
            'donneesPersonnelles_form': donneesPersonnelles_form,
            'address_form' : address_form,
            'city_form' : city_form,
            'zipCode_form' : zipCode_form,
            'sauvegarde' : sauvegarde,
            'context_object_name': Client.objects.all()
            }
    )


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



class VoitureCreate (CreateView):
    model = Motorise
    fields = '__all__'



