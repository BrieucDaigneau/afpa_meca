from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

from django.db import models

        
        
class ZipCode(models.Model):
    zip_code = models.CharField(max_length=15, verbose_name = 'Code Postal',)


    def __str__(self):
        return str( self.zip_code )

    class Meta:
        verbose_name = "Code Postal"
        verbose_name_plural = "Codes Postaux"


class City(models.Model):
    city_name   = models.CharField(max_length =25, verbose_name = "Ville",)
    zip_codes     = models.ManyToManyField(ZipCode, verbose_name="Code Postal")

    def __str__(self):
        return  self.city_name

    class Meta:
        verbose_name = "Ville"
        verbose_name_plural = "Villes"   
     

class Address(models.Model):
    street              = models.TextField(max_length=50, blank=False, verbose_name = "Nom de la rue",)
    street_number       = models.CharField(max_length = 30, null=True, blank = True, verbose_name = "Numéro de la rue",)
    street_complement   = models.CharField(max_length =50, null=True, blank = True, verbose_name = "Complément d'adresse",)

    city    = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')
    zipCode = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')
 
    class Meta:
        verbose_name = "Adresse"

    def __str__(self):
        return self.street_number + " " + str(self.street) + " " + self.street_complement + " " + str(self.zipCode) + " " + str(self.city)

class DonneesPersonnelles(models.Model):
    mail_client = models.EmailField("Email Client", max_length=35, unique=True)
    telephone_client = models.CharField("Téléphone Client", blank=False, max_length=10, null=True)
    carte_AFPA_img = models.ImageField("Carte AFPA", null=True, blank=True, upload_to="img/carte_AFPA_client")

    class Meta:
        verbose_name = "Donnée Personnelle"
        verbose_name_plural = "Données Personnelles"
    def __str__(self) :
        return "Adresse mail : {0}  Téléphone : {1}".format(self.mail_client, self.telephone_client)
        

class Client(models.Model):
    nom_client = models.CharField("Nom Client", max_length=15)
    prenom_client = models.CharField("Prenom Client", max_length=15)
    numero_afpa_client = models.CharField("Numéro carte AFPA Client", max_length=10, default="extérieur")
    donnees_personnelles_client = models.OneToOneField(DonneesPersonnelles, on_delete=models.CASCADE)
    adresse = models.OneToOneField(Address, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}  {1}  N° AFPA : {2}".format(self.nom_client, self.prenom_client, self.numero_afpa_client)


class Vehicule(models.Model):
    # VOITURE = 'VOITURE'
    # MOTO = 'MOTO'
    # VELO = 'VELO'
    
    # Type_vehicule_choice= (
    #     (VOITURE, 'Voiture'),
    #     (MOTO, 'Moto'),
    #     (VELO, 'Velo'),
    # ) 
    
    libelle_modele = models.CharField("libellé modèle", blank=False, max_length=50)
    type_vehicule = ""#models.CharField(
        # max_length = 10,
        # choices=Type_vehicule_choice,
        # default=Type_vehicule_choice[0]
        # )
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)

    def is_upperclass(self):
        return self.type_vehicule in (self.MOTO, self.VOITURE)
    
    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"

    def __str__(self):
        return self.libelle_modele


class Motorise(Vehicule):
    libelle_marque = models.CharField("libellé marque", max_length=100, null=True)
    vin = models.CharField(max_length=100, blank=False, null=True)
    immatriculation = models.CharField( max_length=15, blank=False, null=True)
    kilometrage = models.IntegerField(null=True, blank=True)
    date_mec = models.DateField("date de première m.e.c.", null=True, default=datetime.now )
    carte_grise_img = models.ImageField("carte grise", null=True, blank=False, upload_to="img/carte_grise")
    carte_assurance_img = models.ImageField("carte assurance", null=True, blank=False, upload_to="img/carte_assurance")
    class Meta:
        verbose_name = "Motorisé"
        verbose_name_plural = "Motorisés"

    def __str__(self):
        return self.immatriculation + " " + self.libelle_modele + " " + self.libelle_marque



class Voiture(Motorise):
        
    type_vehicule = "Voiture"
    def __str__(self):
        return Motorise.__str__(self) + " " + self.type_vehicule



class Moto(Motorise):
    type_vehicule = "Moto"
    
    def __str__(self):
        return Motorise.__str__(self) + " " + self.type_vehicule



class Velo(Vehicule):
    type_vehicule = "Velo"
    
    def __str__(self):
        return Vehicule.__str__(self) + " " + self.type_vehicule
        
    class Meta:
        verbose_name = "Vélo"
        verbose_name_plural = "Vélos"


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_entree_stage = models.DateField(null=True, blank=True)
    date_sortie_stage = models.DateField(null=True, blank=True)
    carte_afpa = models.CharField("Numéro carte AFPA", max_length=10, blank=False, )
   
    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class Intervention(models.Model):
    date_saisie_intervention = models.DateTimeField("date d'intervention", null=True, blank=False, default=datetime.now )
    date_restitution_prevu = models.DateField("Date de restitution prévisionnelle", null=True)
    diagnostic = models.TextField(max_length=300, null=True)
    intervention_a_realiser = models.TextField("interventions prévus", max_length=300, null=True)
    intervention_realisee = models.BooleanField("intervention réalisée", null=False, default=False)

   
    ValidationFormateur = 'VF'
    AttenteFormateur = 'AF'
    RefusFormateur = 'RF'
    AttenteDevis = 'AD'
    
    
    Statut_choice = (
        (ValidationFormateur, 'ValidationFormateur'),
        (AttenteFormateur, 'AttenteFormateur'),
        (RefusFormateur, 'RefusFormateur'),
        (AttenteDevis, 'AttenteDevis'),
        
    )
    # if Vehicule.type_vehicule == "Voiture":
    statut = models.CharField(
        max_length = 20,
        choices = Statut_choice,
        default = AttenteDevis,
    )
    # else :
    #         statut = models.CharField(
    #         max_length = 20,
    #         choices = Statut_choice,
    #         default = AttenteFormateur,
    #     )
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vehicule) + " " + str(self.date_saisie_intervention) + " " + str(self.utilisateur) + " " + str(self.statut)

class Piece(models.Model):
    reference_piece = models.CharField("référence pièce", blank=False, max_length=20)
    libelle_piece = models.CharField("libellé de la pièce", blank=False, max_length=50)
    
    class Meta:
        verbose_name = "Pièces"
        verbose_name_plural = "Pièces"

    def __str__(self):
        return self.libelle_piece


class Fournisseur(models.Model):
    libelle_fournisseur = models.CharField("Nom Fournisseur", blank=False, max_length=35)
    piece_fournisseur = models.ManyToManyField(Piece, through='Piece_Fournisseur_Devis')
  
    def __str__(self):
        return self.libelle_fournisseur


class Devis(models.Model):
    def NumeroDevis():
        num = Devis.objects.count()
        if num == None:
            return 1
        else:
            return num +1

    numero_devis = models.IntegerField(unique=True, default=NumeroDevis )
    date_devis = models.DateField("Date du devis", blank=False, null=False)
    devis_signe_img = models.ImageField("Scan du devis signé", null=True, blank=True, upload_to ="img/devis")
    ValidationFormateur = 'VF'
    AttenteFormateur = 'AF'
    RefusFormateur = 'RF'
    ValidationClient ='VC'
    AttenteClient = 'AC'
    RefusClient = 'RC'
    
    Statut_choice = (
        (ValidationFormateur, 'ValidationFormateur'),
        (AttenteFormateur, 'AttenteFormateur'),
        (RefusFormateur, 'RefusFormateur'),
        (ValidationClient,'ValidationClient'),
        (AttenteClient, 'AttenteClient'),
        (RefusClient, 'RefusClient'),
    )
    statut = models.CharField(
        max_length = 20,
        choices = Statut_choice,
        default = AttenteFormateur,
    )

#cléfs de relations
    commande_fournisseur = models.ManyToManyField(Fournisseur, through='Piece_Fournisseur_Devis')
    commande_piece = models.ManyToManyField(Piece, through='Piece_Fournisseur_Devis')


    class Meta():
        verbose_name_plural = "Devis"

    def __str__(self):
        return str(self.numero_devis)


class Piece_Fournisseur_Devis(models.Model):
    quantite_pieces_necessaires = models.IntegerField("Quantité de pièces nécessaires", blank=False, null=True, default=1)
    prix_ht = models.IntegerField("Prix Hors Taxes", null=True, blank=False)
    numero_devis_fournisseur = models.CharField("Numéro du devis fournisseur", max_length=20, null=True, blank=False)
    
#cléfs de relations
    devis = models.ForeignKey(Devis, null=True, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, null=True, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, null=True, on_delete=models.CASCADE)


    class Meta():
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return str(self.fournisseur) + " devis n°" +str(self.devis) + " pièce : " + str(self.piece)

