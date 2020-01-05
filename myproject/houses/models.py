from django.db import models
from django.contrib.gis.db import models as geomodels

from geopy.geocoders import Nominatim


geolocator = Nominatim(timeout=7, user_agent='houses')


class House(models.Model):
    address = models.CharField(max_length=255)
    geometry = geomodels.PointField(verbose_name='Місце на мапі', 
             extent=(31.44, 49.217, 32.47, 49.68), 
             help_text='<em>Просто поставте маркер на карту</em>')
    @property
    def lat_lng(self):
        return list(getattr(self.geometry, 'coords', [])[::-1])
    # TO STRING METHOD
    def __str__(self):
        return f'{self.pk} {self.address}'

    # PREPROCESSING ADDRESS
    def _generate_address(self):
        location = geolocator.reverse((self.geometry.y, self.geometry.x))
        addr = location.address
        addr_split = addr.split(',')
        address = ', '.join(addr_split[:-4])
        self.address = address

    # SAVE METHOD
    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_address()
        super().save(*args, **kwargs)

