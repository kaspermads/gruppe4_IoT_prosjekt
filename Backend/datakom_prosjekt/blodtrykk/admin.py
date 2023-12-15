from django.contrib import admin
from . import models
from django.contrib.auth.models import User

# Register your models here.


admin.site.register(models.Patient)
admin.site.register(models.Nurse)


"""class NurseAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not obj.user:
            # Opprett en tilknyttet User-instans her, om nødvendig
            user = User.objects.create_user(...)
            obj.user = user
        super().save_model(request, obj, form, change)


admin.site.register(models.Nurse, NurseAdmin)"""
