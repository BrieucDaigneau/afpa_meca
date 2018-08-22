from django.contrib import admin
from .models import *
from .models import Utilisateur
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class UtilisateurInline(admin.StackedInline):
    model = Utilisateur
    can_delete = False
    verbose_name_plural = 'Utilisateurs'

class UserAdmin(BaseUserAdmin):
    inlines = (UtilisateurInline, )

class ClientInline(admin.TabularInline):
    model = Client
    can_delete = False

class DonneesPersonnellesAdmin(admin.ModelAdmin):
    inlines = (ClientInline, )

class ZipCodeInline(admin.TabularInline):   
    model = City.zip_codes.through
    verbose_name = "Code Postal"
    verbose_name_plural = "Codes Postaux"
        
class ZipCodeAdmin(admin.ModelAdmin):
    exclude = ("zipCode", )
    inlines = (ZipCodeInline, )

class CityInline(admin.TabularInline):
    model = City.zip_codes.through
    verbose_name = "Ville"

class CityAdmin(admin.ModelAdmin):
    exclude = ("zipCode", )
    inlines = (CityInline, )


# Register your models here.
admin.site.register(Address)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Motorise)
admin.site.register(Moto)
admin.site.register(Voiture)
admin.site.register(Velo)


admin.site.register(Intervention)
admin.site.register(Devis)
admin.site.register(Piece)
admin.site.register(Fournisseur)
admin.site.register(DonneesPersonnelles, DonneesPersonnellesAdmin)
admin.site.register(Piece_Fournisseur_Devis)