from django.contrib import admin
from .models import ParkingSpot, Vehicle

class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'my_address', 'parking_duration', 'is_deleted')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'affiliated_users', 'cookies_consent')

    def save_model(self, request, obj, form, change):
        obj.affiliated_users = request.user
        obj.save()

admin.site.register(ParkingSpot, ParkingSpotAdmin)
admin.site.register(Vehicle, VehicleAdmin)
