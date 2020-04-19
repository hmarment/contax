from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path("contacts/", views.list_or_create_contact, name="list_or_create_contacts"),
    path(
        "contacts/<int:contact_id>",
        views.get_update_or_delete_contact,
        name="get_delete_update_contact",
    ),
    path(
        "contacts/<int:contact_id>/email",
        views.add_contact_email_address,
        name="add_contact_email_address",
    ),
    path(
        "contacts/<int:contact_id>/email/<int:email_id>",
        views.update_or_delete_contact_email_address,
        name="update_or_delete_contact_email_address",
    ),
    path(
        "postal_addresses/",
        views.list_or_add_contact_postal_address,
        name="list_or_add_contact_postal_address",
    ),
    path(
        "postal_addresses/<int:contact_id>",
        views.get_update_or_delete_contact_postal_address,
        name="get_update_or_delete_contact_postal_address",
    ),
]
