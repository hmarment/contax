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
    path("contacts/<int:contact_id>/email", views.contact_add_email_address),
    path(
        "contacts/<int:contact_id>/email/<int:email_id>",
        views.contact_email_address_detail,
    ),
    path("postal_addresses/", views.postal_address_list),
    path("postal_addresses/<int:contact_id>", views.postal_address_detail),
]
