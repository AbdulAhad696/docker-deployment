from django.urls import path
from API_Handler.adm import admin_views

urlpatterns=[
    path('',admin_views.testView),
    # path('patient/<str:wardName>/',admin_views.PatientListCreateView.as_view(),name="get-ward-patient"),
    path('patient/',admin_views.PatientListCreateView.as_view(),name="get-all-add-patients"),
    path('patient/delete/',admin_views.PatientRetrieveUpdateDestroyAPIView.as_view(),name="RUD-patients"),
    path('dashboard/',admin_views.AdminDashboard.as_view(),name="dashboard-data")
]