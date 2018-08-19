from django.urls import path

from django.views.generic import ListView
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .models import Client
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required


app_name = 'garage'

urlpatterns = [  
    # path('client', views.client, name='client'),   
    url(r'login', LoginView.as_view(redirect_authenticated_user=True, template_name="garage/login.html"),
        name='login'),
    url(r'logout', LogoutView.as_view(template_name="garage/logout.html"), name='logout'),
    
    url(r'^recherche/$', login_required(views.recherche), name='recherche'),
    path('accueil/', login_required(views.Accueil.as_view()), name='accueil'),

    path('client-create', login_required(views.ClientCreateView.as_view()), name='client-create'),   
    path('client-select/', login_required(views.ClientSelect.as_view()), name="client-select"),
    path('clients', login_required(views.Clients.as_view()), name="clients"),
    path('client-update/<pk>/', login_required(views.ClientUpdate.as_view()), name='client-update'),

    path('velo-select/<int:client_id>/', login_required(views.VeloSelect.as_view()), name="velo-select"),
    path('velo-create/<int:client_id>/', login_required(views.VeloCreate.as_view()), name='velo-create'),
    path('velos', login_required(views.VeloList.as_view()), name="velos"),
    path('velo-update/<pk>/', login_required(views.VeloUpdate.as_view()), name='velo-update'),

    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('moto-select/<int:client_id>/', login_required(views.MotoSelect.as_view()), name="moto-select"),
    path('moto-create/<int:client_id>/', login_required(views.MotoCreate.as_view()), name='moto-create'),
    path('motos', login_required(views.MotoList.as_view()), name="motos"),
    path('moto-update/<pk>/', login_required(views.MotoUpdate.as_view()), name='moto-update'),

    path('voiture-select/<int:client_id>/', login_required(views.VehiculeSelect.as_view()), name="voiture-select"),
    path('voiture-create/<int:client_id>/', login_required(views.VoitureCreate.as_view()), name='voiture-create'),
    path('voitures', login_required(views.VehiculeList.as_view()), name="voitures"),
    path('nouveau-choix-vehicule', views.ChoixVehicule, name="choixVehicule"),
    path('voiture-update/<pk>/', login_required(views.VoitureUpdate.as_view()), name='voiture-update'),

    # path('reparation/<int:client_id>/', login_required(views.ordre_reparation), name='ordre_reparation'),
    # path('reparation/', login_required(views.ordre_reparation.as_view()), name='ordre_reparation'),
    path('intervention-create/<int:vehicule_id>/', login_required(views.InterventionCreate.as_view()), name='intervention-create'),
    path('interventions', login_required(views.Interventions.as_view()), name="interventions"),
    path('intervention-update/<pk>/', login_required(views.InterventionUpdate.as_view()), name='intervention-update'),

]
