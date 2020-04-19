import pytest

from django.urls import reverse
from rest_framework.test import APIClient

from .models import Contact


@pytest.fixture
def contact_factory(db):
    """Create a contact."""

    def create_contact(first_name, last_name, date_of_birth):
        contact = Contact.objects.create(
            first_name=first_name, last_name=last_name, date_of_birth=date_of_birth,
        )
        return contact

    return create_contact


@pytest.fixture
def contact_1(db, contact_factory):
    return contact_factory(
        first_name="Jane", last_name="Doe", date_of_birth="2000-01-01"
    )


@pytest.fixture
def contact_2(db, contact_factory):
    return contact_factory(
        first_name="John", last_name="Smith", date_of_birth="1990-01-01"
    )


def test_should_create_user(contact_1):
    contact = Contact.objects.get(pk=1)
    assert (
        contact.first_name == "Jane"
        and contact.last_name == "Doe"
        and contact.date_of_birth.isoformat() == "2000-01-01"
    )


def test_should_create_two_users(contact_1, contact_2):
    assert contact_1.pk != contact_2.pk


@pytest.fixture
def client():
    return APIClient()


def test_contact_list_view(client, contact_1):
    response = client.get("/api/contacts/")
    content = response.content.decode()
    assert response.status_code == 200
    assert contact_1.first_name in content and contact_1.last_name in content
