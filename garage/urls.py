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
    url(r'connexion', LoginView.as_view(redirect_authenticated_user=True, template_name="garage/login.html"),
        name='login'),
    url(r'déconnexion', LogoutView.as_view(template_name="garage/logout.html"), name='logout'),
    
    url(r'^recherche/$', login_required(views.recherche), name='search'),
    path('accueil/', login_required(views.Home.as_view()), name='home'),

    path('création-client', login_required(views.CustomerCreateView.as_view()), name='customer-create'),   
    path('sélection-client/', login_required(views.CustomerSelect.as_view()), name="customer-select"),
    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('sélection-moto/<int:customer_id>/', login_required(views.MotorbikeSelect.as_view()), name="motorbike-select"),

    path('sélection-véhicule/<int:customer_id>/', login_required(views.VehicleSelect.as_view()), name="vehicle-select"),
    path('création-voiture/<int:customer_id>/', login_required(views.VehicleCreate.as_view()), name='vehicle-create'),
    path('consultation-vehicules', login_required(views.VehicleList.as_view()), name="vehicles"),
    path('nouveau-choix-vehicule', views.ChoiceVehicle, name="vehicule-choice"),
    
    # path('reparation/<int:client_id>/', login_required(views.ordre_reparation), name='ordre_reparation'),
    # path('reparation/', login_required(views.ordre_reparation.as_view()), name='ordre_reparation'),
    path('création-ordre-réparation/<int:vehicle_id>/', login_required(views.ReparationOrder.as_view()), name='reparation-order-create'),
]
