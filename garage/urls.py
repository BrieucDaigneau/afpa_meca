from django.urls import path
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from . import views

app_name = 'garage'

urlpatterns = [    
    
    url(r'logout', LogoutView.as_view(template_name='garage/logout.html'), name='logout'), 
    path('accueil/', login_required(views.Home.as_view()), name='home'),

    path('creation-client/', login_required(views.CustomerCreateView.as_view()), name='customer-create'),   
    path('selection-client/', login_required(views.CustomerSelect.as_view()), name='customer-select'),
    path('consultation-clients/', login_required(views.Customers.as_view()), name='customers'),
    path('actualisation-client/<pk>/', login_required(views.CustomerUpdate.as_view()), name='customer-update'),  
    
    path('creation-vehicule/<int:customer_id>/', login_required(views.VehicleCreate.as_view()), name='vehicle-create'),
    path('selection-vehicule/<int:customer_id>/', login_required(views.VehicleSelect.as_view()), name='vehicle-select'),
    path('consultation-vehicules/', login_required(views.Vehicles.as_view()), name='vehicles'),
    path('actualisation-vehicule/<pk>/', login_required(views.VehicleUpdate.as_view()), name='vehicle-update'),

    path('creation-intervention/<int:vehicle_id>', login_required(views.ReparationOrderCreateView.as_view()), name='reparation-order-create'),  
    path('consultation-interventions', login_required(views.ReparationOrders.as_view()), name='reparation-orders'),
    path('actualisation-intervention/<pk>/', login_required(views.ReparationOrderUpdate.as_view()), name='reparation-order-update'),
    
    path('creation-devis/<int:reparation_orders_id>/', login_required(views.QuotationCreate.as_view()), name='quotation-create'),      
    path('consultation-devis/', login_required(views.Quotations.as_view()), name='quotations'),
    path('actualisation-devis/<pk>/', login_required(views.QuotationUpdate.as_view()), name='quotation-update'),

    path('car_condition', login_required(views.car_condition), name='car_condition'),    
]

