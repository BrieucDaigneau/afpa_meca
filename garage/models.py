from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

from django.db import models

        
        
class ZipCode(models.Model):
    zip_code = models.CharField(max_length=15, verbose_name = 'Code Postal',)
    
    # def __str__(self):
    #     rslt = ""
    #     nb = 0
    #     for c in self.city_set.all():
    #         if nb != 0:
    #             rslt += " ; "
    #         rslt += str( c )
    #         nb += 1
    #     return str( self.zip_code ) + " " + rslt

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
    street              = models.TextField(max_length=50, verbose_name = "Nom de la rue",)
    street_number       = models.CharField(max_length = 30, null=True, blank = True, verbose_name = "Numéro de la rue",)
    street_complement   = models.CharField(max_length =50, null=True, blank = True, verbose_name = "Complément d'adresse",)

    city    = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = 'Ville')
    zipCode = models.ForeignKey(ZipCode, on_delete=models.CASCADE, verbose_name = 'Code Postal')
 
    class Meta:
        verbose_name = "Adresse"


class DonneesPersonnelles(models.Model):
    mail_client = models.EmailField("Email Client", max_length=35)
    telephone_client = models.CharField("Téléphone Client", max_length=10)
    carte_AFPA_img = models.ImageField("Carte AFPA", null=True, blank=True, upload_to="img/carte_AFPA_client")

    def __str__(self) :
        return "Adresse mail : {0}  Téléphone : {1}".format(self.mail_client, self.telephone_client)
        

class Client(models.Model):
    nom_client = models.CharField("Nom Client", max_length=15)
    prenom_client = models.CharField("Prenom Client", max_length=15)
    numero_afpa_client = models.CharField("Numéro carte AFPA Client", max_length=10, null=True)
    donnees_personnelles_client = models.OneToOneField(DonneesPersonnelles, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}  {1}  N° AFPA : {2}".format(self.nom_client, self.prenom_client, self.numero_afpa_client)


class Vehicule(models.Model):
    VOITURE = 'VOITURE'
    MOTO = 'MOTO'
    VELO = 'VELO'
    
    Type_vehicule_choice= (
        (VOITURE, 'Voiture'),
        (MOTO, 'Moto'),
        (VELO, 'Velo'),
    ) 
    
    libelle_modele = models.CharField("libellé modèle", max_length=50)
    type_vehicule = models.CharField(
        max_length = 10,
        choices=Type_vehicule_choice,
        default=Type_vehicule_choice[0]
        )
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    def is_upperclass(self):
        return self.type_vehicule in (self.MOTO, self.VOITURE)
    
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


class Intervention(models.Model):
    date_saisie_intervention = models.DateTimeField("date d'intervention", null=True, default=datetime.now )
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
    Statut = models.CharField(
        max_length = 20,
        choices = Statut_choice,
        default = AttenteDevis,
    )
    # else :
    #         Statut = models.CharField(
    #         max_length = 20,
    #         choices = Statut_choice,
    #         default = AttenteFormateur,
    #     )
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
class Piece(models.Model):
    reference_piece = models.CharField("référence pièce", max_length=20)
    libelle_piece = models.CharField("libellé de la pièce", max_length=50)
    def __str__(self):
        return self.libelle_piece


class Fournisseur(models.Model):
    libelle_fournisseur = models.CharField("Nom Fournisseur", max_length=35)
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
    
    class Meta():
        verbose_name_plural = "Devis"

    date_devis = models.DateField("Date du devis", null=False)
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
    Statut = models.CharField(
        max_length = 20,
        choices = Statut_choice,
        default = AttenteFormateur,
    )

    commande_fournisseur = models.ManyToManyField(Fournisseur, through='Piece_Fournisseur_Devis')
    commande_piece = models.ManyToManyField(Piece, through='Piece_Fournisseur_Devis')
    
    def __str__(self):
        return str(self.numero_devis)


class Piece_Fournisseur_Devis(models.Model):
    quantite_pieces_necessaires = models.IntegerField("Quantité de pièces nécessaires", null=True)
    prix_ht = models.IntegerField("Prix Hors Taxes", null=True, blank=False)
    numero_devis_fournisseur = models.CharField("Numéro du devis fournisseur", max_length=20, null=True, blank=False)
    devis = models.ForeignKey(Devis, null=True, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, null=True, on_delete=models.CASCADE)
    piece = models.ForeignKey(Piece, null=True, on_delete=models.CASCADE)

    class Meta():
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return str(self.fournisseur) + " devis n°" +str(self.devis) + " pièce : " + str(self.piece)

