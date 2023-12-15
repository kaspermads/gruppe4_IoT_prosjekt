from rest_framework import serializers

from blodtrykk.forms import CustomUserCreationForm
from . import models
from .models import Patient
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserCreationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def validate(self, data):
        form = CustomUserCreationForm(data)
        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password1"],
            email=validated_data["email"],
        )
        return user


class PatientListSerializer(serializers.ModelSerializer):
    added_by = serializers.SerializerMethodField()

    class Meta:
        model = models.Patient
        fields = ["id", "first_name", "last_name", "birthDate", "added_by"]

    # Overrides the get_added_by method to return the full name of the user who added the patient
    def get_added_by(self, obj):
        return obj.added_by.get_full_name() if obj.added_by else "None"


class PatientBloodPressureDataSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.DailyBloodPressureData
        fields = ["patient_id", "systolic", "diastolic",
                  "pulse", "timestamp"]

    # Validates that the patient_id is valid and checks if the patient exists

    def validate_patient_id(self, patient_id):
        try:
            models.Patient.objects.get(id=patient_id)
            return patient_id
        except models.Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist")

    # Overrides the create method to create a new DailyBloodPressureData object with the patient_id sent in the request.
    # The patient_id is removed from the validated_data and the patient is fetched from the database.
    # The DailyBloodPressureData object is then created with the patient and the validated_data.
    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        patient = models.Patient.objects.get(id=patient_id)
        blood_pressure_data = models.DailyBloodPressureData.objects.create(
            patient=patient, **validated_data)
        return blood_pressure_data


class PatientOxygenSaturationDataSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.DailyOxygenSaturationData
        fields = ["patient_id", "timestamp", "oxygen_saturation"]

    # Validates that the patient_id is valid and checks if the patient exists

    def validate_patient_id(self, patient_id):
        try:
            models.Patient.objects.get(id=patient_id)
            return patient_id
        except models.Patient.DoesNotExist:
            raise serializers.ValidationError("Patient does not exist")

    # Overrides the create method to create a new DailyBloodPressureData object with the patient_id sent in the request.
    # The patient_id is removed from the validated_data and the patient is fetched from the database.
    # The DailyBloodPressureData object is then created with the patient and the validated_data.
    def create(self, validated_data):
        patient_id = validated_data.pop("patient_id")
        patient = models.Patient.objects.get(id=patient_id)
        oxygen_saturation_data = models.DailyOxygenSaturationData.objects.create(
            patient=patient, **validated_data)
        return oxygen_saturation_data


class PatientDataSerializer(serializers.ModelSerializer):
    patient_blood_pressure_data = PatientBloodPressureDataSerializer(
        many=True, read_only=True)
    patient_blood_oxygen_saturation_data = PatientOxygenSaturationDataSerializer(
        many=True, read_only=True)

    class Meta:
        model = models.Patient
        fields = "__all__"

    # Overrides the get_added_by method to return the full name of the user who added the patient
    def get_added_by(self, obj):
        return obj.added_by.get_full_name() if obj.added_by else "None"


class PatientRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "birthDate", "phone", "added_by"]
        read_only_fields = ["added_by"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data['added_by'] = user
        return super().create(validated_data)


class NurseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nurse
        fields = "__all__"


class NurseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nurse
        fields = "__all__"


class NurseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",
                  "email"]
