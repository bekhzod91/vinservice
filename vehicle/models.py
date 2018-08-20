from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _


class Vehicle(models.Model):
    DECODE_THIS = 'decodethis'
    DATA_OWNERS = (
        (DECODE_THIS, _('Decode this'))
    )

    vin = models.CharField(max_length=255, unique=True, db_index=True)
    year = models.IntegerField()
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    data = JSONField()
    data_owner = models.CharField(max_length=255, choices=DATA_OWNERS)

    def __str__(self):
        return 'Model: %s, Year: %s Color: %s' % (
            self.model, self.year, self.color
        )
