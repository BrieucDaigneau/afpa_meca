from django.db import models
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
    street              = models.TextField(max_length=50, blank=False, verbose_name = "Nom de la rue",)
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
    phone_number    = models.CharField("Téléphone ", blank=False, max_length=10, null=True)
    afpa_card_img   = models.ImageField("Carte AFPA", null=True, blank=True, upload_to="img/carte_AFPA_client")

    class Meta:
        verbose_name        = "Donnée Personnelle"
        verbose_name_plural = "Données Personnelles"

    def __str__(self) :
        return "Adresse mail : {0}  Téléphone : {1}".format(self.mail, self.phone_number)
        

class Customer(models.Model):
    lastname        = models.CharField("Nom Client", max_length=15)
    firstname       = models.CharField("Prenom Client", max_length=15)
    afpa_number     = models.CharField("Numéro carte AFPA Client", max_length=10, default="extérieur")
    personal_data   = models.OneToOneField(PersonalData, on_delete=models.CASCADE)
    address         = models.OneToOneField(Address, null=True, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return "{0}  {1}  N° AFPA : {2}".format(self.lastname, self.firstname, self.afpa_number)


class MyManager(models.Manager):
    def get_child(self, id):
        if VehicleConfig['vehicle'] == 'car':
            if Car.objects.filter(pk=id):
                return Car.objects.get(pk=id)
        elif VehicleConfig['vehicle'] == 'bike': 
            if Motorbike.objects.filter(pk=id):
                return Motorbike.objects.get(pk=id)
            if Bike.objects.filter(pk=id):
                return Bike.objects.get(pk=id)
        return None


    def filter_child(self, id):
        if VehicleConfig['vehicle'] == 'car' :
            if Car.objects.filter(customer=id) :
                return Car.objects.filter(customer=id)

        if VehicleConfig['vehicle'] == 'bike' : 
            if Motorbike.objects.filter(customer=id) :
                return Motorbike.objects.filter(customer=id)
            if Bike.objects.filter(customer=id) :
                return Bike.objects.filter(customer=id)


    def get_model(self, id):
        if VehicleConfig['vehicle'] == 'car' :
            if Car.objects.filter(pk=id) :
                return Car

        if VehicleConfig['vehicle'] == 'bike' : 
            if Motorbike.objects.filter(pk=id) :
                return Motorbike
            if Bike.objects.filter(pk=id) :
                return Bike



class Vehicle(models.Model):
    model       = models.CharField("libellé modèle", blank=False, max_length=50)
    customer    = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
    objects     = MyManager()

    def __str__(self):
        return self.model
    

class Motorized(Vehicle):
    brand               = models.CharField("libellé marque", max_length=100, null=True)
    vin                 = models.CharField(max_length=100, blank=False, null=True)
    license_plate       = models.CharField( max_length=15, blank=False, null=True)
    mileage             = models.IntegerField(null=True, blank=True)
    circulation_date    = models.DateField("date de première m.e.c.", null=True)
    grey_doc_img        = models.ImageField("carte grise", null=True, blank=False, upload_to="img/carte_grise")
    insurance_img       = models.ImageField("carte assurance", null=True, blank=False, upload_to="img/carte_assurance")

    class Meta:
        verbose_name        = "Motorisé"
        verbose_name_plural = "Motorisés"

    def __str__(self):
        return str(self.license_plate) + " " + str(self.model) + " " + str(self.brand)


class Car(Motorized):
    pass
        

class Motorbike(Motorized):
    pass


class Bike(Vehicle):
    pass


class UserProfile(models.Model):
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    beginning_intership = models.DateField(null=True, blank=True)
    ending_internship   = models.DateField(null=True, blank=True)
    afpa_card           = models.CharField("Numéro carte AFPA", max_length=10, blank=False, )
   
    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class ReparationOrder(models.Model):
    committed_date          = models.DateTimeField("date d'intervention", null=True, blank=False, default=datetime.now )
    return_date             = models.DateField("Date de restitution prévisionnelle", null=True)
    diagnostic              = models.TextField(max_length=300, null=True)
    to_do_actions           = models.TextField("interventions prévus", max_length=300, null=True)
    actions_done            = models.BooleanField("intervention réalisée", null=False, default=False)
    
    AwaitingInstructor   = "AI"
    InstructorValidation = "IV"
    InstructorDenial     = "ID"
    AwaitingEstimate     = "AE"

    Status_choice           = (
        (AwaitingInstructor, 'AttenteFormateur'),
        (InstructorValidation, 'ValidationFormateur'),
        (InstructorDenial, 'RefusFormateur'),
        (AwaitingEstimate, 'AttenteDevis'),  
    )
    status                  = models.CharField(
        max_length  = 20,
        choices     = Status_choice,
        default     = Status_choice[0]
    )
    user_profile            = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle                 = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="reparation_order")

    def __str__(self):
        return str(self.vehicle) + " " + str(self.committed_date) + " " + str(self.user_profile) + " " + str(self.status)


class Component(models.Model):
    reference   = models.CharField("référence pièce", blank=False, max_length=20)
    name        = models.CharField("libellé de la pièce", blank=False, max_length=50)
    
    class Meta:
        verbose_name        = "Pièces"
        verbose_name_plural = "Pièces"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name        = models.CharField("Nom Fournisseur", blank=False, max_length=35)
    components  = models.ManyToManyField(Component, through='Component_Supplier_Estimate', related_name="suppliers")
  
    def __str__(self):
        return self.name


class Estimate(models.Model):
    number          = models.IntegerField(unique=True )
    date            = models.DateField("Date du devis", blank=False, null=False)
    signed_img      = models.ImageField("Scan du devis signé", null=True, blank=True, upload_to ="img/devis")  
    
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
    status          = models.CharField(
        max_length      = 20,
        choices         = Status_choice,
        default         = Status_choice[0],
    )
    suppliers       = models.ManyToManyField(Supplier, through='Component_Supplier_Estimate', related_name="estimates")
    components      = models.ManyToManyField(Component, through='Component_Supplier_Estimate', related_name="estimates")

    class Meta():
        verbose_name_plural = "Devis"

    def __str__(self):
        return str(self.number)


class Component_Supplier_Estimate(models.Model):
    quantity            = models.IntegerField("Quantité de pièces nécessaires", blank=False, null=True, default=1)
    price               = models.IntegerField("Prix Hors Taxes", null=True, blank=False)
    estimate_supplier   = models.CharField("Numéro du devis fournisseur", max_length=20, null=True, blank=False)
    estimate            = models.ForeignKey(Estimate, null=True, on_delete=models.CASCADE, related_name="connection")
    supplier            = models.ForeignKey(Supplier, null=True, on_delete=models.CASCADE, related_name="connection")
    component           = models.ForeignKey(Component, null=True, on_delete=models.CASCADE, related_name="connection")

    class Meta():
        verbose_name        = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return str(self.supplier) + " devis n°" +str(self.estimate) + " pièce : " + str(self.component)

