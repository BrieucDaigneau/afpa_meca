from django.http import HttpResponse
from .models import *

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm, DonneesPersonnellesForm
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from . import urls


def client(request):
    sauvegarde = False
    client_form = ClientForm(request.POST or None)   
    donneesPersonnelles_form = DonneesPersonnellesForm(request.POST or None)
    if client_form.is_valid() and donneesPersonnelles_form.is_valid():
        donnees = donneesPersonnelles_form.save()
        client = client_form.save(commit=False)
        client.donnees_personnelles_client = donnees
        client.save()
        
        sauvegarde = True
        return redirect("garage:ordre_reparation", client_id=client.id)

    return render(
        request, 
        'garage/client_form.html', 
        {   'client_form': client_form,
            'donneesPersonnelles_form': donneesPersonnelles_form,
            'sauvegarde' : sauvegarde,
            'context_object_name': Client.objects.all()}
    )


def ordre_reparation(request, client_id):
    client = Client.objects.get(pk=client_id)
    context = {
        'client': client
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

class VehiculeSelect(ListView):
    
    # def mon_model(self, request):
    #         if request.POST.get('optradio') == "Voiture":
    model = Voiture
            # elif Vehicule.type_vehicule == "Moto":
            #     model = Moto
            # elif Vehicule.type_vehicule == "Velo":
            #     model = Velo
    #         return model
    # model = mon_model()

    template_name = 'garage/vehicule-select.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for v in self.get_queryset():
            print( v)
        context['liste_vehicule'] = self.get_queryset()
        context['isVoiture'] = self.model == Voiture
        context['isMoto'] = self.model == Moto
        context['isVelo'] = self.model == Velo

        return context
   
class VehiculeList(VehiculeSelect):
    template_name = 'garage/vehicules.html'

   
def ChoixVehicule(request):
    pass

