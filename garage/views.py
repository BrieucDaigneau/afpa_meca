from django.http import HttpResponse
from .models import *

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


class DeuxiemeEtape(ListView):
    # if Vehicule.type_vehicule == "Voiture":
    model = Voiture
    # elif Vehicule.type_vehicule == "Moto":
    #     model = Moto
    # elif Vehicule.type_vehicule == "Velo":
    #     model = Velo
    template_name = 'garage/etape-2.html'
    paginate_by = 12
    # success_url = reverse_lazy('garage:ordre_reparation')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        for v in self.get_queryset():
            print( v)
        
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print( "#############", os.path.join(BASE_DIR, 'toto.txt') )

        context['liste_vehicule'] = self.get_queryset()
        return context
    def get_absolute_url(self):
        return reverse('garage:ordre_reparation', kwargs={'pk':self.pk})

def ChoixVehicule(request):
    pass