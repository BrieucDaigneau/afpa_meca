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



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Vehicule)
admin.site.register(Motorise)
admin.site.register(Moto)
admin.site.register(Voiture)
admin.site.register(Velo)
admin.site.register(TypeVehicule)

admin.site.register(Intervention)
admin.site.register(Devis)
admin.site.register(Piece)
admin.site.register(Fournisseur)