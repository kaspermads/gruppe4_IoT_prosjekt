from django.db import models
from django.contrib.auth.models import User


# Create your models here.


#How patients are stored in the database
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthDate = models.DateField(null=True)
    phone = models.IntegerField(null=True)
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="pasient")
    address = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):

        super(Patient, self).save(*args, **kwargs)

#How blood pressure data is stored in the database
class DailyBloodPressureData(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, related_name="patient_blood_pressure_data")
    systolic = models.IntegerField()
    diastolic = models.IntegerField()
    pulse = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

#How oxygen saturation data is stored in the database
class DailyOxygenSaturationData(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, related_name="patient_blood_oxygen_saturation_data")
    oxygen_saturation = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

#How Nurse data is stored in the database
class Nurse(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthDate = models.DateField(null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
