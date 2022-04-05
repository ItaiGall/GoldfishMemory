from django.db import models
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django_google_maps import fields as map_fields
from django.urls import reverse



class ParkingSpot(models.Model):

    location_type = "Parking Spot"
    user = models.ForeignKey(User, editable=False, null=True, blank=False, on_delete=models.CASCADE)
    slug = models.CharField(max_length=30, editable=False, unique=True, null=True, blank=False)
    recording_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    start_parking = models.DateTimeField(null=True, blank=True)
    stop_parking = models.DateTimeField(null=True, blank=True)
    my_timezone = models.CharField(max_length=30, null=True, blank=False)
    parking_duration = models.DurationField(null=True, blank=True)
    my_latitude = models.FloatField(null=True, blank=False)
    my_longitude = models.FloatField(null=True, blank=False)
    my_geolocation = map_fields.GeoLocationField(max_length=100, default=None, null=True, blank=True)
    my_address = map_fields.AddressField(max_length=200, default=None, null=True, blank=True)
    thumb = models.ImageField(default='placeholder-image.png', blank=True)
    is_deleted = models.BooleanField(default=False, blank=False)

    def get_absolute_url(self):
        return reverse('GoldfishMemory_App:parkingspot_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return str(self.user) + "," + str(self.start_parking)

    class Meta:
        verbose_name_plural = "Parking Spots DB"
        ordering = ['start_parking']

class Vehicle(models.Model):
    license_number = models.CharField(max_length=30, null=True, blank=False)
    cookies_consent = models.BooleanField(default=False, blank=False)
    affiliated_users = models.ForeignKey(User, editable=False, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.license_number)
