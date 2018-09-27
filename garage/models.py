from django.db import models
from django import forms
from django.contrib.auth.models import User

from datetime import datetime

from afpa_meca.business_application import VehicleConfig

class Address(models.Model):
    city               = models.CharField(verbose_name = "Ville", max_length=100, null=True)
    zip_code           = models.CharField(verbose_name = "CP", max_length=20, null=True)
    street_name        = models.CharField(verbose_name = "Rue", max_length=200, null=True)
    street_number      = models.CharField(verbose_name = "N° de Rue", max_length=10, null=True, blank=True)
    street_complement  = models.CharField(verbose_name = "Complément d'addresse", max_length =50, null=True, blank = True)    
    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
  

class PersonalData(models.Model):
    mail            = models.EmailField(verbose_name = "Email ", max_length=35, unique=True)
    phone_number    = models.CharField(verbose_name = "Téléphone ", max_length=10, null=True)
    afpa_card_img   = models.ImageField(verbose_name = "Carte AFPA", null=True, blank=True, upload_to="img/carte_AFPA_client")

    class Meta:
        verbose_name        = "Donnée Personnelle"
        verbose_name_plural = "Données Personnelles"

    def __str__(self) :
        return "Adresse mail : {0}  Téléphone : {1}".format(self.mail, self.phone_number)
        

class Customer(models.Model):
    lastname        = models.CharField(verbose_name = "Nom Client", max_length=15)
    firstname       = models.CharField(verbose_name = "Prenom Client", max_length=15)
    afpa_number     = models.CharField(verbose_name = "Numéro carte AFPA Client", max_length=10)
    personal_data   = models.OneToOneField(PersonalData, verbose_name = "Données personnelles", on_delete=models.CASCADE)
    address         = models.OneToOneField(Address, null=True, verbose_name = "Adresse", on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return "{0}  {1}  N° AFPA : {2}".format(self.lastname, self.firstname, self.afpa_number)

# surchpk= du manager django pour le modele vehicle
# Car Bike et Motorbike héritent tous de Vehicle
# donc vehicle_id == car_id ou bike_id ou motorbike_id
class MyManager(models.Manager):
    
# récupère les voitures pour l'app car, et les motos/velos pour l'app bike
# dans un dico de véhicules passé en paramètre
    def filter_type(self, dico): # pas d'accés à la bdd
        if VehicleConfig['vehicle'] == 'bike':         
            return [ v for v in dico if isinstance(v, Bike) or isinstance(v, Motorbike) ]
        elif VehicleConfig['vehicle'] == 'car':
            return [ v for v in dico if isinstance(v, Car) ]

# récupère le modèle enfant (voiture/moto/velo) 
# en fonction de l'id du véhicule passé en paramètre
    def get_model(self, id):
        if Car.objects.filter(pk=id):
            return Car
        elif Motorbike.objects.filter(pk=id):
            return Motorbike
        elif Bike.objects.filter(pk=id):
            return Bike

    def get_child(self, id):
        return self.get_model( id ).objects.get(pk=id)

    def filter_child(self, id):
        return self.get_model( id ).objects.filter(pk=id)

# filtre un dico de véhicules par application (car/bike) et par id_client
# et retourne un dico avec les modèles correspondants (voiture ou velo/moto)
    def filter_by_user(self, id_customer):
        # on suppose qu'un client aurra tout au plus 5 véhicules
        vehicles =  self.filter(customer=id_customer) 
        typed_vehicles = [self.get_child(v.id) for v in vehicles ]
        return self.filter_type( typed_vehicles )


class Vehicle(models.Model):
    model_name  = models.CharField("Libellé modèle", max_length=50)
    customer    = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, verbose_name = "Client")
    objects     = MyManager()

    def __str__(self):
        return self.model_name
    

class Motorized(Vehicle):
    brand               = models.CharField(verbose_name = "Libellé marque", max_length=100, null=True)
    vin                 = models.CharField(verbose_name = "VIN", max_length=100, null=True)
    license_plate       = models.CharField(verbose_name = "Immatriculation",  max_length=15, null=True)
    mileage             = models.IntegerField(verbose_name = "Kilometrage", null=True, blank=True)
    circulation_date    = models.DateField(verbose_name = "Date de première m.e.c.", null=True)
    grey_doc_img        = models.ImageField(verbose_name = "Carte grise", null=True, upload_to="img/carte_grise")
    insurance_img       = models.ImageField(verbose_name = "Carte assurance", null=True, upload_to="img/carte_assurance")

    class Meta:
        verbose_name        = "Motorisé"
        verbose_name_plural = "Motorisés"

    def __str__(self):
        return str(self.license_plate) + " " + str(self.model_name) + " " + str(self.brand)


class Car(Motorized):
    pass
        

class Motorbike(Motorized):
    pass


class Bike(Vehicle):
    pass


class UserProfile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    beginning_intership = models.DateField("Début du stage", null=True)
    ending_internship   = models.DateField("Fin du stage", null=True)
    afpa_card           = models.CharField("Numéro carte AFPA", max_length=10, )
   
    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class ReparationOrder(models.Model):
    number                  = models.CharField(verbose_name = "N° ordre de rep.", unique=True, null=True, max_length=15)
    committed_date          = models.DateTimeField(verbose_name = "Date de reception", null=True, default=datetime.now )
    return_date             = models.DateField(verbose_name = "Date de restitution prévisionnelle", null=True)
    diagnostic              = models.TextField(verbose_name = "Diagnostique", max_length=300, null=True)
    to_do_actions           = models.TextField(verbose_name = "Interventions prévus", max_length=300, null=True)
    actions_done            = models.BooleanField(verbose_name = "Intervention réalisée", null=False, default=False)
    
    Status_choice           = (
        ( "AttenteFormateur"    , 'AttenteFormateur'),
        ( "ValidationFormateur" , 'ValidationFormateur'),
        ("RefusFormateur"       , 'RefusFormateur'),
        ("AttenteDevis"         , 'AttenteDevis'),  
    )
    status                  = models.CharField(
        max_length  = 20,
        choices     = Status_choice,
        default     = "AttenteFormateur"
    )
    user_profile            = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "Réceptionnaire")
    vehicle                 = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name = "Véhicule", related_name="reparation_order")

    def __str__(self):
        return str(self.number) + " ---- " + str(self.vehicle) + "  ----  " + str(self.committed_date) + "   ----   " + str(self.user_profile) + "    ---------------------    " + str(self.status)

    class Meta:
        verbose_name    = "Ordre de Réparations"
        verbose_name_plural = "Ordres de Réparations"
    
class Supplier(models.Model):
    name         = models.CharField("Nom Fournisseur", max_length=35)
        
    def __str__(self):
        return self.name
    class Meta:
        verbose_name        = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

class Component(models.Model):
    quantity     = models.IntegerField(verbose_name = "Quantité pièce")
    reference   = models.CharField(verbose_name = "Référence pièce", max_length=20)
    name        = models.CharField(verbose_name = "Libellé de la pièce", max_length=50)
    price       = models.FloatField(verbose_name = "Prix unitaire")

    supplier    = models.ForeignKey(Supplier, verbose_name = "Fournisseur", on_delete=models.CASCADE, related_name="components")
    quotation   = models.ForeignKey('Quotation', verbose_name = "Devis", on_delete=models.CASCADE, related_name='components')
    class Meta:
        verbose_name        = "Pièces"
        verbose_name_plural = "Pièces"

    def __str__(self):
        return self.name


class Quotation(models.Model):
    payoff_choice   = ( ("Chèques", 'Chèques'), ("Espèces", 'Espèces'), )
    Status_choice   = ( ("AttenteFormateur", 'AttenteFormateur'), ("ValidationFormateur", 'ValidationFormateur'),
                        ("RefusFormateur", 'RefusFormateur'), ("ValidationClient",'ValidationClient'),
                        ("AttenteClient", 'AttenteClient'), ("RefusClient", 'RefusClient'), )

    number                  = models.CharField(verbose_name = "n° Devis", unique=True, max_length=15)
    date                    = models.DateField(verbose_name = "Date du devis", null=False, default=datetime.now)
    signed_img              = models.ImageField(verbose_name = "Scan du devis signé", null=True, upload_to ="img/devis") 
    payoff_date             = models.DateField(verbose_name = "Date de paiement", null=True)
    payoff_type             = models.CharField(verbose_name = "Moyen de paiement", max_length=7, null=True, choices=payoff_choice, default=payoff_choice[0],)
    status                  = models.CharField(verbose_name = "statut", max_length=20,choices=Status_choice,default="AttenteFormateur",)
    amount                  = models.FloatField(verbose_name = "Total TTC")
    num_quotation_supplier  = models.CharField(verbose_name = "N° devis Fournisseur", max_length=15)

    user_profile            = models.ForeignKey(User, verbose_name = "Réceptionnaire", on_delete=models.CASCADE)
    reparation_order        = models.ForeignKey(ReparationOrder, verbose_name = "Ordre de réparation attaché", on_delete=models.CASCADE, related_name="quotation")
    supplier                = models.ForeignKey(Supplier, verbose_name = "Fournisseur", related_name="quotations", on_delete=models.CASCADE)
    

    class Meta():
        verbose_name_plural = "Devis"

    def __str__(self):
        return str(self.number) + " ---- " + str(self.reparation_order.number) + " ---- " + str(self.reparation_order.vehicle) + "  ----  " + str(self.date) + "   ----   " + str(self.user_profile) + "    ---------------------    " + str(self.status)

