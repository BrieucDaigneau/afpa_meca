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
    path('accueil/', login_required(views.accueil), name='accueil'),

    path('client-create', login_required(views.ClientCreateView.as_view()), name='client-create'),   
    path('client-select/', login_required(views.ClientSelect.as_view()), name="client-select"),
    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('moto-select/<int:client_id>/', login_required(views.MotoSelect.as_view()), name="moto-select"),

    path('voiture-select/<int:client_id>/', login_required(views.VehiculeSelect.as_view()), name="voiture-select"),
    path('voiture-create/<int:client_id>/', login_required(views.VoitureCreate.as_view()), name='voiture-create'),
    path('vehicules', login_required(views.VehiculeList.as_view()), name="vehicules"),
    path('nouveau-choix-vehicule', views.ChoixVehicule, name="choixVehicule"),
    
    path('reparation/<int:client_id>/<int:address_id>/<int:zipCode_id>/<int:city_id>/', login_required(views.ordre_reparation), name='ordre_reparation'),
    #  path('reparation/<int:voiture_id>/', login_required(views.ordre_reparation), name='ordre_reparation'),
]
