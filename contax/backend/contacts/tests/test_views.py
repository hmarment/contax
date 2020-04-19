import pytest
import json

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from contacts.models import Contact, EmailAddress
from contacts.serializers import ContactSerializer


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


@pytest.fixture
def valid_email_payload(contact_1):
    """Return valid payload for updating an email address."""
    return {
        "contact_id": contact_1.pk,
        "name": "New Email Address Name",
        "email_address": f"{contact_1.first_name}@{contact_1.last_name}.com",
    }


@pytest.fixture
def invalid_email_payload(contact_1):
    """Return valid payload for updating an email address."""
    return {
        "contact_id": contact_1.pk,
        "name": "Personal",
        "email_address": "not-a-valid-email-address",
    }


# tests for list_or_create_contact method
def test_list_or_create_contact__get_all_contacts(client, contact_1, contact_2):
    """Fetch contacts from API and compare to database query."""

    # fetch via API
    response = client.get(reverse("list_or_create_contacts"))
    # get data from db
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


def test_list_or_create_contact__create_valid_contact(
    client, db, valid_contact_payload
):
    """Test creating a contact via API."""
    response = client.post(
        reverse("list_or_create_contacts"),
        data=json.dumps(valid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_list_or_create_contact__create_invalid_contact(
    client, db, invalid_contact_payload
):
    """Test that invalid input returns an error."""

    response = client.post(
        reverse("list_or_create_contacts"),
        data=json.dumps(invalid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# tests for get_update_or_delete_contact method
def test_get_update_or_delete_contact__get_valid_single_contact(client, contact_1):
    """Test fetching an existing contact."""
    response = client.get(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk})
    )
    contact = Contact.objects.get(pk=contact_1.pk)
    serializer = ContactSerializer(contact)
    assert response.data == serializer.data
    assert response.status_code == status.HTTP_200_OK


def test_get_update_or_delete_contact__get_invalid_single_contact(client, db):
    """Test fetching a contact that does not exist."""
    response = client.get(
        reverse("get_delete_update_contact", kwargs={"contact_id": 30})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_update_or_delete_contact__valid_update_contact(
    client, db, contact_1, valid_contact_payload
):
    """Test updating an existing contact."""
    response = client.put(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps(valid_contact_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_update_or_delete_contact__invalid_update_contact(
    client, db, contact_1, invalid_contact_payload
):
    response = client.put(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps(invalid_contact_payload),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_update_or_delete_contact__valid_delete_contact(client, db, contact_1):
    """Test deletion of an existing contact."""
    response = client.delete(
        reverse("get_delete_update_contact", kwargs={"contact_id": contact_1.pk})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_update_or_delete_contact__invalid_delete_contact(client, db):
    """Test deletion of a non-existent contact."""
    response = client.delete(
        reverse("get_delete_update_contact", kwargs={"contact_id": 30})
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


# tests for add_contact_email_address method
def test_add_contact_email_address__valid(client, db, contact_1):
    """Test adding a valid email address to a contact."""

    email_address = f"{contact_1.first_name}@{contact_1.last_name}.com"

    response = client.post(
        reverse("add_contact_email_address", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps({"name": "Personal", "email_address": email_address}),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_add_contact_email_address__invalid(client, db, contact_1):
    """Test adding an invalid email address to a contact."""

    email_address = f"{contact_1.first_name}{contact_1.last_name}.com"

    response = client.post(
        reverse("add_contact_email_address", kwargs={"contact_id": contact_1.pk}),
        data=json.dumps({"name": "Personal", "email_address": email_address}),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_add_contact_email_address__existing(client, db, contact_1_email):
    """Test adding an existing email address to a contact."""

    response = client.post(
        reverse(
            "add_contact_email_address",
            kwargs={"contact_id": contact_1_email.contact.pk},
        ),
        data=json.dumps(
            {
                "name": contact_1_email.name,
                "email_address": contact_1_email.email_address,
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


# tests for update_or_delete_contact_email_address method
def test_update_or_delete_contact_email_address__update_existing_valid(
    client, db, contact_1_email, valid_email_payload
):
    """Test updating an existing email address with a valid request."""

    response = client.put(
        reverse(
            "update_or_delete_contact_email_address",
            kwargs={
                "contact_id": contact_1_email.contact.pk,
                "email_id": contact_1_email.pk,
            },
        ),
        data=json.dumps(valid_email_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_or_delete_contact_email_address__update_existing_invalid(
    client, db, contact_1_email, invalid_email_payload
):
    """Test updating an existing email address with an invalid request."""

    response = client.put(
        reverse(
            "update_or_delete_contact_email_address",
            kwargs={
                "contact_id": contact_1_email.contact.pk,
                "email_id": contact_1_email.pk,
            },
        ),
        data=json.dumps(invalid_email_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_or_delete_contact_email_address__update_nonexistent(
    client, db, contact_1, valid_email_payload
):
    """Test updating a non-existent email address."""

    response = client.put(
        reverse(
            "update_or_delete_contact_email_address",
            kwargs={"contact_id": contact_1.pk, "email_id": 30},
        ),
        data=json.dumps(valid_email_payload),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_or_delete_contact_email_address__delete_existing(
    client, db, contact_1_email
):
    """Test deleting an existing email address."""
    response = client.delete(
        reverse(
            "update_or_delete_contact_email_address",
            kwargs={
                "contact_id": contact_1_email.contact.pk,
                "email_id": contact_1_email.pk,
            },
        ),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
