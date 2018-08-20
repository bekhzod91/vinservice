# REST framework
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound

# Project
from .models import Vehicle
from .serializers import VehicleSerializer
from .utils import get_vehicle_by_vin


class VehicleView(RetrieveAPIView):
    model = Vehicle
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    lookup_field = 'vin'

    # If you want disable "Decode this" remove this method
    def get_object(self):
        vin = self.kwargs.get('vin')
        queryset = self.filter_queryset(self.get_queryset())

        try:
            return queryset.get(vin=vin)
        except self.model.DoesNotExist:
            vehicle = get_vehicle_by_vin(vin)
            instance = self.model.create_by_decodethis(vehicle)

            if not instance:
                raise NotFound

            return instance
