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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Supplier)
admin.site.register(Quotation)
admin.site.register(ReparationOrder)
admin.site.register(Component)

