from django.urls import path
from . import views


app_name = 'garage'

urlpatterns = [
    path('client', views.client, name='client'),    
    path('reparation/<int:client_id>/', views.ordre_reparation, name='reparation'),    
]