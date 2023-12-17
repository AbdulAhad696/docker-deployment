from django.contrib import admin

# Register your models here.
from .models import Lookup, Patient, Users, Ward, Doctor, Medication, MedicationSchedule, Nurse, Documents, CareVitals

#SNP register
admin.site.register(Lookup)
admin.site.register(Users)
admin.site.register(Ward)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Medication)
admin.site.register(Nurse)
admin.site.register(MedicationSchedule)
admin.site.register(Documents)
admin.site.register(CareVitals)