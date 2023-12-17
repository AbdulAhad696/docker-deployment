# example/urls.py
from django.urls import path

from API_Handler.views import index,fetch_from_influx,count_influx,fetch_images_ids,fetchUserSpecificData
from API_Handler.signIn import getSpecificUser
from API_Handler.signUp import postUserData
from .user_access import UserAccessView
from .update_token import UpdateTokenView
from .user_access import ActivityListView
from API_Handler.doctor import doctor_views as dw



# ----------
# from .user_access import ActivateEmailView
# ---------

urlpatterns = [
    path('', index),
    path('fetch/',fetch_from_influx),
    path('count/',count_influx),
    path('image_id/',fetch_images_ids),
    path('fetchUserData/',fetchUserSpecificData),
    path('userData/',postUserData),
    path('user/<str:email>/<str:password>/<str:isAuthenticatedByGoogle>/',getSpecificUser),
    path('sign-in/', UserAccessView.as_view(), name='signin'),
    path('sign-in-desktop/', UserAccessView.as_view(), name='signin-desktop'),
    path('sign-up/', UserAccessView.as_view(), name='signup'),
    path('updatetoken/', UpdateTokenView.as_view(), name='updatetoekn'),
    path('activities/', ActivityListView.as_view(),name='activity-list' ),

    # # ----------
    path('activate/<uidb64>/<token>',UserAccessView.activate,name='activate'),
    # # ----------
    
]