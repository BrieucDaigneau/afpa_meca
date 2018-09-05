from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Utilisateurs'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

class CustomerInline(admin.TabularInline):
    model = Customer
    can_delete = False

class PersonalDataAdmin(admin.ModelAdmin):
    inlines = (CustomerInline, )

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


admin.site.register(Address)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Motorized)
admin.site.register(Motorbike)
admin.site.register(Car)
admin.site.register(Bike)
admin.site.register(ReparationOrder)
admin.site.register(Estimate)
admin.site.register(Component)
admin.site.register(Supplier)
admin.site.register(PersonalData, PersonalDataAdmin)
admin.site.register(Component_Supplier_Estimate)