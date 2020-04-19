import pytest

from contacts.models import Contact


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
