from django.urls import path
from . import views


app_name = 'GoldfishMemory_App'
urlpatterns = [
    path('create_ps/', views.create_parking_spot, name='create_ps'),
    path('finalize_ps/', views.finalize_parking_spot, name='finalize_ps'),
    path('parkingspot_list/', views.PSListView.as_view(), name='parkingspot_list'),
    path('parkingspot_detail/<slug:slug>/', views.PSDetailView.as_view(), name='parkingspot_detail'),
]