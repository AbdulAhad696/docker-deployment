from django.db import models
import datetime

class Lookup(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.TextField()
    value = models.TextField()

    def _str_(self):
        return self.value


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50, default="example@gmail.com")
    password = models.TextField()
    user_type = models.ForeignKey(
        Lookup, on_delete=models.CASCADE, related_name="user_type", null=True
    )
    contact = models.CharField(max_length=12, blank=True, null=True)
    first_name = models.CharField(max_length=15, null=True)
    cnic = models.CharField(max_length=13, null=True)
    last_name = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=250, null=True)
    gender = models.ForeignKey(
        Lookup,
        on_delete=models.CASCADE,
        related_name="gender_type",
        blank=True,
        null=True,
    )
    profile_picture = models.TextField(blank=True, null=True)
    is_authenticated_by_google = models.BooleanField(null=True)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)

    def _str_(self):
        return str(self.user_name)


class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default="Hospital Name")


class Ward(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.SmallIntegerField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE,null=True)
    def _str_(self):
        return self.name

class Patient(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    nursing_diagnosis = models.TextField(blank=True)
    medical_diagnosis = models.TextField(blank=True)
    cnic = models.CharField(max_length=13, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    bmi = models.FloatField(blank=True)
    weight = models.SmallIntegerField(blank=True)
    height = models.CharField(max_length=5, blank=True)
    systolic_bp = models.SmallIntegerField()
    diastolic_bp = models.SmallIntegerField()
    heart_beat = models.SmallIntegerField()
    temperature = models.SmallIntegerField()
    o2_level = models.SmallIntegerField()
    blood_group = models.CharField(max_length=2, blank=True)
    hospitalization = models.TextField(blank=True)
    major_illness = models.TextField(blank=True)
    surgeries = models.TextField(blank=True)
    pain_location = models.TextField(blank=True)
    pain_severity = models.TextField(blank=True)
    current_medication = models.TextField(blank=True)
    past_medication = models.TextField(blank=True)
    supplements = models.TextField(blank=True)
    medical_allergy = models.TextField(blank=True)
    admission_date = models.DateTimeField(blank=False,default=datetime.datetime.now)
    discharge_date = models.DateTimeField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id','admission_date'],name='unique_id_admission_constraint'
            )
        ]


    def _str_(self):
        return str(self.id)


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    domain = models.ForeignKey(Lookup, on_delete=models.CASCADE,related_name="doctor_domain",null=True)
    experience = models.SmallIntegerField(null=True)
    bio = models.CharField(max_length=50, null=True)

    def _str_(self):
        return self.user.first_name + self.user.last_name


class Diagnosis(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis_date = models.DateTimeField()
    diagnosis_notes = models.TextField()

    def _str_(self):
        return f"Diagnosis for {self.patient} by {self.doctor}"


class Medication(models.Model):
    id = models.AutoField(primary_key=True)
    med_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    prescribed_to = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    current = models.BooleanField()

    def _str_(self):
        return self.med_name


class Nurse(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.ForeignKey(Lookup, on_delete=models.CASCADE,related_name="nurse_type")
    experience = models.SmallIntegerField(null=True)
    bio = models.CharField(max_length=50, null=True)

    def _str_(self):
        return self.id


class NurseWard(models.Model):
    id = models.AutoField(primary_key=True)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def _str_(self):
        return self.nurse+self.ward
    
class DoctorWard(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def _str_(self):
        return self.doctor+self.ward

class MedicationSchedule(models.Model):
    med = models.ForeignKey(Medication, on_delete=models.CASCADE)
    administered_by = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    date_administered = models.DateField()
    time_administered = models.TimeField()

    def _str_(self):
        return self.med


class Documents(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    link = models.CharField(max_length=255)

    def _str_(self):
        return self.name

class CareVitals(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time = models.TimeField()
    date = models.DateField()
    systolic_bp = models.SmallIntegerField()
    diastolic_bp = models.SmallIntegerField()
    heart_rate = models.SmallIntegerField()
    temperature = models.FloatField()
    spo2 = models.SmallIntegerField()
    respiration_rate = models.SmallIntegerField()

    def _str_(self):
        return self.patient


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    time_stamp = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True)
    activity_type = models.ForeignKey(
        Lookup, on_delete=models.CASCADE, related_name="activity_type"
    )
    location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def _str_(self):
        return self.activity_type