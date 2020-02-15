from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path("contacts/", views.contact_list),
    path("contacts/<int:pk>", views.contact_detail),
    path("postal_addresses/", views.postal_address_list),
    path("postal_addresses/<int:pk>", views.postal_address_detail),
]
