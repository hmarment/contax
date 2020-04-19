import pytest
import json

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from .models import Contact
from .serializers import ContactSerializer


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
    """Create a first test contact."""
    return contact_factory(
        first_name="Jane", last_name="Doe", date_of_birth="2000-01-01"
    )


@pytest.fixture
def contact_2(db, contact_factory):
    """Create a second test contact."""
    return contact_factory(
        first_name="John", last_name="Smith", date_of_birth="1990-01-01"
    )


def test_should_create_user(contact_1):
    """Test creating a user directly in the database."""
    contact = Contact.objects.get(pk=1)
    assert (
        contact.first_name == "Jane"
        and contact.last_name == "Doe"
        and contact.date_of_birth.isoformat() == "2000-01-01"
    )


def test_should_create_two_users(contact_1, contact_2):
    """Test creating two contacts in the database and ensure they are distinct."""
    assert contact_1.pk != contact_2.pk


@pytest.fixture
def client():
    """Create an API client for testing."""
    return APIClient()


@pytest.fixture
def valid_contact_payload():
    """Return valid payload for creating a contact."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "2020-01-01",
        "email_addresses": [],
        "phone_numbers": [],
    }


@pytest.fixture
def invalid_contact_payload():
    """Return invalid payload for creating a contact."""
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "not-a-valid-date",
        "email_addresses": [],
        "phone_numbers": [],
    }


def test_get_all_contacts(client, contact_1, contact_2):
    """Fetch contacts from API and compare to database query."""

    # fetch via API
    response = client.get(reverse("list_or_create_contacts"))
    # get data from db
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


def test_get_valid_single_contact(client, contact_1):
    """Test fetching an existing contact."""
    response = client.get(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk})
    )
    contact = Contact.objects.get(pk=contact_1.pk)
    serializer = ContactSerializer(contact)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


def test_get_invalid_single_contact(client, db):
    """Test fetching a contact that does not exist."""
    response = client.get(
        reverse("get_delete_update_contact", kwargs={"contact_id": 30})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_valid_contact(client, db, valid_contact_payload):
    """Test creating a contact via API."""
    response = client.post(
        reverse("list_or_create_contacts"),
        data=json.dumps(valid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_invalid_contact(client, db, invalid_contact_payload):
    """Test that invalid input returns an error."""

    response = client.post(
        reverse("list_or_create_contacts"),
        data=json.dumps(invalid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_valid_update_contact(client, db, contact_1, valid_contact_payload):
    """Test updating an existing contact."""
    response = client.put(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps(valid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_invalid_update_contact(client, db, contact_1, invalid_contact_payload):
    response = client.put(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps(invalid_contact_payload),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_valid_delete_contact(client, db, contact_1):
    """Test deletion of an existing contact."""
    response = client.delete(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_invalid_delete_puppy(client, db):
    """Test deletion of a non-existent contact."""
    response = client.delete(
        reverse("get_delete_update_contact", kwargs={"contact_id": 30})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
