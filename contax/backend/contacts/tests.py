import pytest

from .models import Contact


@pytest.fixture
def contact_1(db):
    contact = Contact.objects.create(
        first_name="First", last_name="Last", date_of_birth="2000-01-01"
    )
    return contact


def test_create_user(db, contact_1):
    contact = Contact.objects.get(pk=1)
    assert (
        contact.first_name == "First"
        and contact.last_name == "Last"
        and contact.date_of_birth.isoformat() == "2000-01-01"
    )
