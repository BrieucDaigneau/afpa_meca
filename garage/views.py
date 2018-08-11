from django.http import HttpResponse
from .models import Client, DonneesPersonnelles

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm, DonneesPersonnellesForm
from django.views.generic import CreateView, ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy


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



def clients(request):
    clients = Client.objects.order_by('nom_client')
    donnees_persos = DonneesPersonnelles.objects.order_by('mail_client')
    context = {
        'clients': clients,
        'donnees_persos': donnees_persos
    }
    return render(request, 'garage/clients.html', context )
