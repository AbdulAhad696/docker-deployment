from django.urls import path
from API_Handler.nurse.nurse_views import testView,emptyView

urlpatterns=[
    path('',emptyView),
    path('patient/',testView),
]