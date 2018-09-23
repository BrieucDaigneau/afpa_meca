from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from afpa_meca.business_application import VehicleConfig

class Address(models.Model):
    city               = models.CharField(max_length=100, null=True, verbose_name = 'Ville')
    zip_code           = models.CharField(max_length=20, null=True, verbose_name = 'Code Postal')
    street_name        = models.CharField(max_length=200, null=True, verbose_name = "Nom de la rue")
    street_number      = models.CharField(max_length=10, null=True, blank=True, verbose_name = "Numéro de la rue")
    street_complement  = models.CharField(max_length =50, null=True, blank = True, verbose_name = "Complément d'adresse",)    
    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'
  

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
    
    AwaitingInstructor   = "AttenteFormateur"
    InstructorValidation = "ValidationFormateur"
    InstructorDenial     = "RefusFormateur"
    AwaitingEstimate     = "AttenteDevis"

    Status_choice           = (
        (AwaitingInstructor, 'AttenteFormateur'),
        (InstructorValidation, 'ValidationFormateur'),
        (InstructorDenial, 'RefusFormateur'),
        (AwaitingEstimate, 'AttenteDevis'),  
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


class Component(models.Model):
    reference   = models.CharField("référence pièce", max_length=20)
    name        = models.CharField("libellé de la pièce", max_length=50)
    
    class Meta:
        verbose_name        = "Pièces"
        verbose_name_plural = "Pièces"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name        = models.CharField("Nom Fournisseur", max_length=35)
    components  = models.ManyToManyField(Component, through='Component_Supplier_Estimate', related_name="suppliers")
  
    def __str__(self):
        return self.name


class Estimate(models.Model):
    number            = models.IntegerField(unique=True )
    date              = models.DateField("Date du devis", null=False)
    signed_img        = models.ImageField("Scan du devis signé", null=True, blank=True, upload_to ="img/devis")  
    
    AwaitingInstructor      = "AI"
    InstructorValidation    = "IV"
    InstructorDenial        = "ID"
    CustomerDenial          = "CD"
    ApprovalCustomer        = "ApC"
    AwaitingCustomer        = "AwC"
    
    Status_choice   = (
        ("AwaitingInstructor", 'AttenteFormateur'),
        ("InstructorValidation", 'ValidationFormateur'),
        ("InstructorDenial", 'RefusFormateur'),
        ("ApprovalCustomer",'ValidationClient'),
        ("AwaitingCustomer", 'AttenteClient'),
        ("CustomerDenial", 'RefusClient'),
    )
    status            = models.CharField(
        max_length      = 20,
        choices         = Status_choice,
        default         = Status_choice[0],
    )
    suppliers         = models.ManyToManyField(Supplier, through='Component_Supplier_Estimate', related_name="estimates")
    components        = models.ManyToManyField(Component, through='Component_Supplier_Estimate', related_name="estimates")
    reparation_order  = models.ForeignKey(ReparationOrder, on_delete=models.CASCADE, related_name="estimate")

    class Meta():
        verbose_name_plural = "Devis"

    def __str__(self):
        return str(self.number)


class Component_Supplier_Estimate(models.Model):
    quantity            = models.IntegerField("Quantité de pièces nécessaires", null=True, default=1)
    price               = models.IntegerField("Prix Hors Taxes", null=True)
    estimate_supplier   = models.CharField("Numéro du devis fournisseur", max_length=20, null=True)
    estimate            = models.ForeignKey(Estimate, null=True, on_delete=models.CASCADE, related_name="connection")
    supplier            = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, related_name="connection")
    component           = models.ForeignKey(Component, null=True, on_delete=models.CASCADE, related_name="connection")

    class Meta():
        verbose_name        = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return str(self.supplier) + " devis n°" +str(self.estimate) + " pièce : " + str(self.component)

