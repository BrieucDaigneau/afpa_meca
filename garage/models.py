from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class TypeVehicule(models.Model):
    # libelle_type_vehicule = models.CharField("type de véhicule", max_length=10)
    Voiture = 'voiture'
    Moto = 'moto'
    Velo = 'velo'
    
    Type_vehicule_choice= (
        (Voiture, 'Voiture'),
        (Moto, 'Moto'),
        (Velo, 'Velo'),
    )
    Type_vehicule = models.CharField(
        max_length = 10,
        choices = Type_vehicule_choice,
        default = Voiture,
    )
    
    def __str__(self) :
        return self.libelle_type_vehicule

class Vehicule(models.Model):
    libelle_modele = models.CharField("libellé modèle", max_length=50)
    type_vehicule = models.ForeignKey(TypeVehicule, on_delete=models.CASCADE) 
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

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_entree_stage = models.DateField(null=True, blank=True)
    date_sortie_stage = models.DateField(null=True, blank=True)
    carte_afpa = models.CharField("Numéro carte AFPA", max_length=10, null=False)
    def __str__(self):
        return "Profil de {0}".format(self.user.username)

class Statut(models.Model):
    #libelle_statut = models.CharField("libellé statut", max_length=50)
    ValidationFormateur = 'VF'
    AttenteFormateur = 'AF'
    RefusFormateur = 'RF'
    AttenteDevis = 'AD'
    ValidationClient ='VC'
    AttenteClient = 'AC'
    RefusClient = 'RC'
    
    Statut_choice = (
        (ValidationFormateur, 'ValidationFormateur'),
        (AttenteFormateur, 'AttenteFormateur'),
        (RefusFormateur, 'RefusFormateur'),
        (AttenteDevis, 'AttenteDevis'),
        (ValidationClient,'ValidationClient'),
        (AttenteClient, 'AttenteClient'),
        (RefusClient, 'RefusClient'),
    )

    def StatutDefaut():
        pass

    Statut = models.CharField(
        max_length = 20,
        choices = Statut_choice,
        default = AttenteFormateur,
    )



class Intervention(models.Model):
    date_saisie_intervention = models.DateTimeField("date d'intervention", null=True, default=datetime.now )
    date_restitution_prevu = models.DateField("Date de restitution prévisionnelle", null=True)
    diagnostic = models.TextField(max_length=300, null=True)
    intervention_a_realiser = models.TextField("interventions prévus", max_length=300, null=True)
    intervention_realisee = models.BooleanField("intervention réalisée", null=False, default=False)

class Piece(models.Model):
    reference_piece = models.CharField("référence pièce", max_length=20)
    libelle_piece = models.CharField("libellé de la pièce", max_length=50)
    def __str__(self):
        return self.libelle_piece

class Fournisseur(models.Model):
    libelle_fournisseur = models.CharField("Nom Fournisseur", max_length=35)
    def __str__(self):
        return self.libelle_fournisseur

class Devis(models.Model):
    date_devis = models.DateField("Date du devis", null=False)
    devis_signe_img = models.ImageField("Scan du devis signé", null=True, blank=True, upload_to ="img/devis")
    def NumeroDevis():
        num = Devis.objects.count()
        if num == None:
            return 1
        else:
            return num +1
    numero_devis = models.IntegerField(unique=True, default=NumeroDevis )
    class Meta():
        verbose_name_plural = "Devis"
    
    def __str__(self):
        return self.numero_devis

class Piece_Fournisseur_Devis(models.Model):
    pass