from django.urls import path
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'garage'

urlpatterns = [    
    url(r'login', LoginView.as_view(redirect_authenticated_user=True, template_name='garage/login.html'),
        name='login'),
    url(r'logout', LogoutView.as_view(template_name='garage/logout.html'), name='logout'), 

    # url(r'^recherche/$', login_required(views.search), name='search'),
    path('accueil/', login_required(views.Home.as_view()), name='home'),

    path('creation-client', login_required(views.CustomerCreateView.as_view()), name='customer-create'),   
    path('selection-client/', login_required(views.CustomerSelect.as_view()), name='customer-select'),
    path('consultation-clients', login_required(views.Customers.as_view()), name='customers'),
    path('actualisation-client/<pk>/', login_required(views.CustomerUpdate.as_view()), name='customer-update'),  
    
    path('creation-vehicule/<int:customer_id>/', login_required(views.VehicleCreate.as_view()), name='vehicle-create'),
    path('selection-vehicule/<int:customer_id>/', login_required(views.VehicleSelect.as_view()), name='vehicle-select'),
    path('consultation-vehicles', login_required(views.Vehicles.as_view()), name='vehicles'),
    path('actualisation-vehicule/<pk>/', login_required(views.VehicleUpdate.as_view()), name='vehicle-update'),

    path('creation-intervention/<int:vehicle_id>', login_required(views.ReparationOrderCreateView.as_view()), name='reparation-order-create'),  
    path('actualisation-intervention/<pk>/', login_required(views.ReparationOrderUpdate.as_view()), name='reparation-order-update'), 
    path('car_condition', login_required(views.car_condition), name='car_condition'),
]
    # path('consultation-interventions'), login_required(views.ReparationOrders.as_view()), name='reparation-orders'),





######################################################################################################################################""
    # path('selection-moto/<int:customer_id>/', login_required(views.MotorbikeSelect.as_view()), name='motorbike-select'),
    # path('sélection-véhicule/<int:customer_id>/', login_required(views.VehicleSelect.as_view()), name='vehicle-select'),

    # path('creation-voiture/<int:customer_id>/', login_required(views.CarCreate.as_view()), name='vehicle-create'),
    # path('consultation-vehicules', login_required(views.VehicleList.as_view()), name='vehicles'),      
    # path('creation-ordre-réparation/<int:vehicle_id>/', login_required(views.ReparationOrder.as_view()), name='reparation-order-create'),
