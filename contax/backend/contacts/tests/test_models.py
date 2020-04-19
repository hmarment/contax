import pytest

from contacts.models import Contact


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
