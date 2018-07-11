from django.db import models
from datetime import datetime

# Create your models here.

class Type(models.Model):
    libelle_type_vehicule = models.CharField("type de véhicule", max_length=10)
    def __str__(self) :
        return self.libelle_type_vehicule


class Vehicule(models.Model):
    libelle_modele = models.CharField("libellé modèle", max_length=50)
    type_vehicule = models.ForeignKey(Type, on_delete=models.CASCADE) 
    def __str__(self):
        return self.libelle_modele

class Motorise(Vehicule):
    libelle_marque = models.CharField("libellé marque", max_length=100, null=True)
    vin = models.CharField(max_length=100, null=True)
    immatriculation = models.CharField( max_length=15, null=True)
    kilometrage = models.IntegerField(null=True)
    date_mec = models.DateField("date de première m.e.c.", null=True, default=datetime.now )
    carte_grise_img = models.ImageField("carte grise", null=True, blank=True, upload_to="img/carte_grise")
    carte_assurance_img = models.ImageField("carte assurance", null=True, blank=True, upload_to="img/carte_assurance")

class Voiture(Motorise):
    pass

class Moto(Motorise):
    pass

class Velo(Vehicule): 
    pass
