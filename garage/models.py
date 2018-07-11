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

fatal: HttpRequestException encountered.
   Une erreur s'est produite lors de l'envoi de la demande.
Username for 'https://github.com': Jeffnad
Password for 'https://Jeffnad@github.com':
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 361 bytes | 0 bytes/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed 
fatal: HttpRequestException encountered.
   Une erreur s'est produite lors de l'envoi de la demande.
Username for 'https://github.com': Jeffnad
Password for 'https://Jeffnad@github.com':
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 361 bytes | 0 bytes/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed 
fatal: HttpRequestException encountered.
   Une erreur s'est produite lors de l'envoi de la demande.
Username for 'https://github.com': Jeffnad
Password for 'https://Jeffnad@github.com':
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 361 bytes | 0 bytes/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed 
fatal: HttpRequestException encountered.
   Une erreur s'est produite lors de l'envoi de la demande.
Username for 'https://github.com': Jeffnad
Password for 'https://Jeffnad@github.com':
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 361 bytes | 0 bytes/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed 
fatal: HttpRequestException encountered.
   Une erreur s'est produite lors de l'envoi de la demande.
Username for 'https://github.com': Jeffnad
Password for 'https://Jeffnad@github.com':
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (4/4), 361 bytes | 0 bytes/s, done.
Total 4 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed 
