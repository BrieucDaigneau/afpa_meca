from django.db import models
from django import forms
from django.contrib.auth.models import User

from datetime import datetime

from afpa_meca.business_application import VehicleConfig

        
class ZipCode(models.Model):
    zip_code = models.CharField(max_length=15, verbose_name = 'Code Postal',)

    def __str__(self):
        return str( self.zip_code )

    class Meta:
        verbose_name        = "Code Postal"
        verbose_name_plural = "Codes Postaux"


class City(models.Model):
    city_name   = models.CharField(max_length =25, verbose_name = "Ville",)
    zip_codes   = models.ManyToManyField(ZipCode, verbose_name="Code Postal")

    def __str__(self):
        return  self.city_name

    class Meta:
        verbose_name        = "Ville"
        verbose_name_plural = "Villes"   
     

class Address(models.Model):
    street              = models.TextField(max_length=50, verbose_name = "Nom de la rue",)
    street_number       = models.CharField(max_length = 30, null=True, blank = True, verbose_name = "Numéro de la rue",)
    street_complement   = models.CharField(max_length =50, null=True, blank = True, verbose_name = "Complément d'adresse",)
    city                = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')
    zipCode             = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')
 
    class Meta:
        verbose_name = "Adresse"

    def __str__(self):
        return self.street_number + " " + str(self.street) + " " + self.street_complement + " " + str(self.zipCode) + " " + str(self.city)


class PersonalData(models.Model):
    mail            = models.EmailField("Email ", max_length=35, unique=True)
    phone_number    = models.CharField("Téléphone ", max_length=10, null=True)
    afpa_card_img   = models.ImageField("Carte AFPA", null=True, blank=True, upload_to="img/carte_AFPA_client")

    class Meta:
        verbose_name        = "Donnée Personnelle"
        verbose_name_plural = "Données Personnelles"

    def __str__(self) :
        return "Adresse mail : {0}  Téléphone : {1}".format(self.mail, self.phone_number)
        

class Customer(models.Model):
    lastname        = models.CharField("Nom Client", max_length=15)
    firstname       = models.CharField("Prenom Client", max_length=15)
    afpa_number     = models.CharField("Numéro carte AFPA Client", max_length=10)
    personal_data   = models.OneToOneField(PersonalData, on_delete=models.CASCADE)
    address         = models.OneToOneField(Address, null=True, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return "{0}  {1}  N° AFPA : {2}".format(self.lastname, self.firstname, self.afpa_number)

# surcharge du manager django pour le modele vehicle
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
        # many access to base but not to many
        # on suppose qu'un client aurra tout au plus 5 véhicules
        vehicles =  self.filter(customer=id_customer) 
        typed_vehicles = [self.get_child(v.id) for v in vehicles ]
        return self.filter_type( typed_vehicles )



class Vehicle(models.Model):
    model_name  = models.CharField("libellé modèle", max_length=50)
    customer    = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    objects     = MyManager()

    def __str__(self):
        return self.model_name
    

class Motorized(Vehicle):
    brand               = models.CharField("libellé marque", max_length=100, null=True)
    vin                 = models.CharField(max_length=100, null=True)
    license_plate       = models.CharField( max_length=15, null=True)
    mileage             = models.IntegerField(null=True, blank=True)
    circulation_date    = models.DateField("date de première m.e.c.", null=True)
    grey_doc_img        = models.ImageField("carte grise", null=True, upload_to="img/carte_grise")
    insurance_img       = models.ImageField("carte assurance", null=True, upload_to="img/carte_assurance")

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
    beginning_intership = models.DateField(null=True)
    ending_internship   = models.DateField(null=True)
    afpa_card           = models.CharField("Numéro carte AFPA", max_length=10, )
   
    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class ReparationOrder(models.Model):
    committed_date          = models.DateTimeField("date de reception", null=True, default=datetime.now )
    return_date             = models.DateField("Date de restitution prévisionnelle", null=True)
    diagnostic              = models.TextField(max_length=300, null=True)
    to_do_actions           = models.TextField("interventions prévus", max_length=300, null=True)
    actions_done            = models.BooleanField("intervention réalisée", null=False, default=False)
    
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
    user_profile            = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle                 = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="reparation_order")

    def __str__(self):
        return str(self.vehicle) + " " + str(self.committed_date) + " " + str(self.user_profile) + " " + str(self.status)


class Supplier(models.Model):
    name         = models.CharField("Nom Fournisseur", max_length=35)
        
    def __str__(self):
        return self.name

class Component(models.Model):
    reference   = models.CharField("référence pièce", max_length=20)
    name        = models.CharField("libellé de la pièce", max_length=50)
    price       = models.FloatField("prix unitaire")
    quantity     = models.IntegerField("quantité pièce")

    supplier    = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="components")
    quotation   = models.ForeignKey('Quotation', on_delete=models.CASCADE, related_name='components')
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

    number                  = models.CharField(unique=True, max_length=15)
    date                    = models.DateField("Date du devis", null=False, default=datetime.now)
    signed_img              = models.ImageField("Scan du devis signé", null=True, upload_to ="img/devis") 
    payoff_date             = models.DateField("Date de paiement", null=True)
    payoff_type             = models.CharField(max_length=7, null=True, choices=payoff_choice, default=payoff_choice[0],)
    status                  = models.CharField( max_length=20,choices=Status_choice,default=Status_choice[0],)
    amount                  = models.FloatField("Total TTC")
    num_quotation_supplier  = models.CharField("Numéro devis Fournisseur", max_length=15)

    user_profile            = models.ForeignKey(User, on_delete=models.CASCADE)
    reparation_order        = models.ForeignKey(ReparationOrder, on_delete=models.CASCADE, related_name="quotation")
    supplier                = models.ForeignKey(Supplier, related_name="quotations", on_delete=models.CASCADE)
    

    class Meta():
        verbose_name_plural = "Devis"

    def __str__(self):
        return str(self.number)

# class QuotationLine(models.Model):
    
#     component = models.ForeignKey(Component, related_name='line', on_delete=models.DO_NOTHING,)
#     quotation  = models.ForeignKey(Quotation, related_name='line', on_delete=models.DO_NOTHING,)
    

# class Component_Supplier_Quotation(models.Model):
#     quantity            = models.IntegerField("Quantité de pièces nécessaires", null=True, default=1)
#     price               = models.IntegerField("Prix Hors Taxes", null=True)
#     quotation_supplier   = models.CharField("Numéro du devis fournisseur", max_length=20, null=True)
#     quotation            = models.ForeignKey(Quotation, null=True, on_delete=models.CASCADE, related_name="connection")
#     supplier            = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, related_name="connection")
#     component           = models.ForeignKey(Component, null=True, on_delete=models.CASCADE, related_name="connection")

    # class Meta():
    #     verbose_name        = "Commande"
    #     verbose_name_plural = "Commandes"

    # def __str__(self):
    #     return str(self.supplier) + " devis n°" +str(self.quotation) + " pièce : " + str(self.component)


    