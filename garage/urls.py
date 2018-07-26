from django.urls import path

from django.views.generic import ListView
from . import views

from .models import Client
from django.conf.urls import url

app_name = 'garage'

urlpatterns = [  
    # path('client', views.client, name='client'),   
    path('client-create', views.clientCreate, name='client-create'),   
    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('reparation/<int:client_id>/', views.ordre_reparation, name='ordre_reparation'),
    url(r'^recherche/$', views.recherche, name='recherche'),
    # url(r'^search/$', views.recherche, name='recherche'),
]