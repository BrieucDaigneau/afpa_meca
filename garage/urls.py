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
    path('client-create', login_required(views.ClientCreateView.as_view()), name='client-create'),   
    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('reparation/<int:client_id>/', login_required(views.ordre_reparation), name='ordre_reparation'),
    url(r'^recherche/$', views.recherche, name='recherche'),
    # url(r'^search/$', views.recherche, name='recherche'),
    path('vehicule-select/<int:client_id>/', views.VehiculeSelect.as_view(), name="vehicule-select"),
    path('nouveau-choix-vehicule', views.ChoixVehicule, name="choixVehicule"),
    path('vehicules', views.VehiculeList.as_view(), name="vehicules"),
    url(r'login', LoginView.as_view(redirect_authenticated_user=True, template_name="garage/login.html"),
        name='login'),
    url(r'logout', LogoutView.as_view(template_name="garage/logout.html"), name='logout'),
    path('accueil/', login_required(views.accueil), name='accueil'),
    path('moto-select/<int:client_id>/', views.MotoSelect.as_view(), name="moto-select"),

    # path('garage/login/', include('django.contrib.auth.urls'), name="login"),
]