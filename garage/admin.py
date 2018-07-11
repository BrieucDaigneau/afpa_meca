from django.contrib import admin
from .models import Moto, Voiture, Velo, Type

# Register your models here.

admin.site.register(Moto)
admin.site.register(Voiture)
admin.site.register(Velo)
admin.site.register(Type)