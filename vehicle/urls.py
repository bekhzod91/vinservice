# Django
from django.urls import path

# REST framework
from .views import VehicleView

app_name = 'vehicle'

urlpatterns = [
    path('vehicle/<str:vin>/vin/', VehicleView.as_view(), name='vin')
]
