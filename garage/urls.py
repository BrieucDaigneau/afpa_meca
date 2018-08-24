from django.urls import path
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'garage'

urlpatterns = [    
    url(r'login', LoginView.as_view(redirect_authenticated_user=True, template_name="garage/login.html"),
        name='login'),
    url(r'logout', LogoutView.as_view(template_name="garage/logout.html"), name='logout'), 
    url(r'^recherche/$', login_required(views.search), name='search'),
    path('accueil/', login_required(views.Home.as_view()), name='home'),
    path('creation-client', login_required(views.CustomerCreateView.as_view()), name='customer-create'),   
    path('selection-client/', login_required(views.CustomerSelect.as_view()), name="customer-select"),
    path('clients/', login_required(views.Customers.as_view()), name="customers"),
    path('selection-moto/<int:customer_id>/', login_required(views.MotorbikeSelect.as_view()), name="motorbike-select"),
    path('selection-vehicule/<int:customer_id>/', login_required(views.VehicleSelect.as_view()), name="vehicle-select"),
    path('creation-voiture/<int:customer_id>/', login_required(views.CarCreate.as_view()), name='vehicle-create'),
    path('consultation-vehicules', login_required(views.VehicleList.as_view()), name="vehicles"),      
    path('creation-ordre-reparation/<int:vehicle_id>/', login_required(views.ReparationOrder.as_view()), name='reparation-order-create'),
]

