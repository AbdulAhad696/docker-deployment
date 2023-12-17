from django.urls import path

from .patient_views import PatientAccessView

# from API_Handler.patient.patient_views import testView
# from API_Handler.patient.patient_views import patientAdmission123
urlpatterns = [
    # path('',testView),
    path("patient-register/", PatientAccessView.as_view()),
]
