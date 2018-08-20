from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from .utils import get_vehicle_property, path_or


class Vehicle(models.Model):
    CUSTOM = 'custom'
    DECODE_THIS = 'decodethis'
    DATA_OWNERS = (
        (CUSTOM, _('Custom')),
        (DECODE_THIS, _('Decode this')),
    )

    vin = models.CharField(max_length=255, unique=True, db_index=True)
    year = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    data = JSONField(blank=True, null=True)
    data_owner = models.CharField(
        max_length=255, choices=DATA_OWNERS, default=CUSTOM
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Model: %s, Year: %s Color: %s' % (
            self.model, self.year, self.color
        )

    @classmethod
    def create_by_decodethis(cls, vehicle):
        is_valid = path_or(vehicle, ['decode', 'Valid'])

        if is_valid == 'False':
            return None

        vin = path_or(vehicle, ['decode', 'VIN'])
        year = get_vehicle_property(vehicle, 'Model Year')
        make = get_vehicle_property(vehicle, 'Make')
        model = get_vehicle_property(vehicle, 'Model')
        body_type = get_vehicle_property(vehicle, 'Body Style')
        color = get_vehicle_property(vehicle, 'Exterior Color')
        dimensions = get_vehicle_property(vehicle, 'Turning Diameter')
        weight = get_vehicle_property(vehicle, 'Curb Weight-automatic')

        return cls.objects.create(
            vin=vin, year=year, make=make, model=model,
            type=body_type, color=color, dimensions=dimensions,
            weight=weight, data=vehicle, data_owner=cls.DECODE_THIS
        )
