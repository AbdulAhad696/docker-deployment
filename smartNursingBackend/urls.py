"""vercel_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from API_Handler import views
from django.urls import path, include
# from API_Handler.nurse import nurse_urls
# from API_Handler.doctor import doctor_urls
# from API_Handler.patient import patient_urls
# from API_Handler.adm import admin_urls
from API_Handler import testViews
# from rest_framework import routers

urlpatterns = [
    path('', include('API_Handler.urls')),
    path('admin/', admin.site.urls),
    path('userData/', include('API_Handler.urls')),
    path('user/<str:email>/<str:password>/<str:isAuthenticatedByGoogle>/', include('API_Handler.urls')),
    path('fetch/', include('API_Handler.urls')),
    path('count/',include('API_Handler.urls')),
    path('fetchUserData/',include('API_Handler.urls')),
    path('image_id/',include('API_Handler.urls')),
    # path('books/', testViews.BookListCreateView.as_view()),
    
    # Segregating all User URLS
    path('patient/',include('API_Handler.patient.patient_urls')),
    path('nurse/',include('API_Handler.nurse.nurse_urls')),
    path('doctor/',include('API_Handler.doctor.doctor_urls')),

    path('adm/',include('API_Handler.adm.admin_urls')),
    
    path('sign-in/',include('API_Handler.urls')),
    path('sign-up/',include('API_Handler.urls')),
    path('sign-in-desktop/', include('API_Handler.urls')),
    path('queryBard/',include('API_Handler.doctor.doctor_urls')),

]
