from django.http import HttpResponse
from .models import Client

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ClientForm
from django.views.generic.list import ListView


# class ListeClients(ListView):
#     model = Client
#     context_object_name = "derniers_clients"
#     template_name = "garage/client_list.html"


def ordre_reparation(request, client_id):
    client = Client.objects.get(pk=client_id)
    context = {
        'client': client
    }
    # client = get_object_or_404(Client, id=id)
    return render(request, 'garage/reparation.html', context)    


def client(request):
    sauvegarde = False
    form = ClientForm(request.POST or None)    
    if form.is_valid():
        client = Client()
        client.nom_client = form.cleaned_data["nom_client"]
        client.prenom_client = form.cleaned_data["prenom_client"]
        client.telephone_client = form.cleaned_data["telephone_client"]        
        client.email_client = form.cleaned_data["email_client"]    
        client.adresse_client = form.cleaned_data["adresse_client"]
        client.code_postal_client = form.cleaned_data["code_postal_client"]
        client.ville_client = form.cleaned_data["ville_client"]
        client.pays_client = form.cleaned_data["pays_client"]
        client.save()
        sauvegarde = True
        return redirect("garage:reparation", client_id=client.id)

    return render(
        request, 
        'garage/list_creer_client.html', 
        {   'form': form,
            'sauvegarde' : sauvegarde,
            'context_object_name': Client.objects.all()}
    )




