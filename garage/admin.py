from django.contrib import admin
from .models import Vehicule, Motorise, Moto, Voiture, Velo, Type

# Register your models here.

admin.site.register(Vehicule)
admin.site.register(Motorise)
admin.site.register(Moto)
admin.site.register(Voiture)
admin.site.register(Velo)
admin.site.register(Type)