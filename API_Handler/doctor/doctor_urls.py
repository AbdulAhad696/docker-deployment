from django.urls import path
from API_Handler.doctor.doctor_views import QueryBard as qb

from .doctor_views import add_doctor,get_hospital_doctors,delete_doctor,get_doctor_by_id,get_doctors_domains,get_hospital_ward,update_doctor,get_domains_wards



urlpatterns = [
    path("query/",qb.as_view(),name="queryBard"),
    path("hospital/wards/", get_hospital_ward, name="get-hospital-wards"),
    path("hospital/", get_hospital_doctors, name="get-hospital-doctors"),
    path("domains/", get_doctors_domains, name="get-doctors-domains"),
    path("add/", add_doctor, name="add-doctors"),
    path("delete/", delete_doctor, name="delete-doctors"),
    path("id/", get_doctor_by_id, name="get-doctor-by-id"),
    path("update/", update_doctor, name="update-doctor"),
    path("domains-wards/", get_domains_wards, name="get-domains-wards"),
]
