from django.urls import path

from django.views.generic import ListView
from . import views

from django.contrib.auth.views import LoginView
from .models import Client
from django.conf.urls import url

app_name = 'garage'

urlpatterns = [
    path('client-create', views.ClientCreate.as_view(), name='client-create'),    
    # path('client', views.client, name='client'),   BAA a reactiver Liste et creation client 
    # path('client/<int:client_id>/', views.modifier_client, name='modifier'),    
    path('reparation/<int:client_id>/', views.ordre_reparation, name='reparation'),
    url(r'^recherche/$', views.recherche, name='recherche'),
    # url(r'^search/$', views.recherche, name='recherche'),
    url(r'^login', LoginView.as_view(redirect_authenticated_user=True, template_name="garage/login.html"),
        name='login'),
]

