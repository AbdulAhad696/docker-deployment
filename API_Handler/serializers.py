from rest_framework import serializers
from .models import (
    Lookup,
    Patient,
    Users,
    Ward,
    Doctor,
    Medication,
    MedicationSchedule,
    DoctorWard,
    Nurse,
    Documents,
    Hospital,
    CareVitals,
    Activity,
)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"

class LookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lookup
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source='gender.value', required = False)
    class Meta:
        model = Users
        fields = ["profile_picture","user_name","address" , "cnic", "contact","email" , 'date_of_birth',"first_name" , "last_name" ,'is_verified','is_authenticated_by_google','user_type','gender']
        # fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    domain = serializers.CharField(source = 'domain.value')  # Include User information
    class Meta:
        model = Doctor
        fields = "__all__"

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"

class WardSerializer(serializers.ModelSerializer):
    # hospital = HospitalSerializer()
    class Meta:
        model = Ward
        fields = "__all__"

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = "__all__"

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"

class MedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationSchedule
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = "__all__"

class VitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareVitals
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    activityName = serializers.CharField(source="activityType.Value")
    class Meta:
        model = Activity
        fields = "__all__"

class DoctorWardSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    ward = serializers.CharField(source='ward.name')
    class Meta:
        model = DoctorWard
        fields = "__all__"
