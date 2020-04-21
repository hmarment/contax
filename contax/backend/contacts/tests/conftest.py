import pytest

from contacts.models import Contact, EmailAddress, PostalAddress


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
def email_factory(db):
    """Create an email address."""

    def create_email_address(contact, name, email_address):
        email = EmailAddress.objects.create(
            contact=contact, name=name, email_address=email_address,
        )
        return email

    return create_email_address


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


@pytest.fixture
def contact_1_email(db, contact_1, email_factory):
    """Add an email address to test contact 1."""
    email_address = f"{contact_1.first_name}@{contact_1.last_name}.com"
    return email_factory(
        contact=contact_1, name="Personal", email_address=email_address
    )


@pytest.fixture
def postal_address_factory(db):
    """Create a postal address."""

    def create_address(street, city, post_code, country, state=None):
        address = PostalAddress.objects.create(
            street=street, city=city, post_code=post_code, country=country, state=state
        )
        return address

    return create_address


@pytest.fixture
def postal_address_1(db, postal_address_factory):
    """Create a first test address."""
    return postal_address_factory(
        street="10 Downing Street", city="London", post_code="SW1A 2AA", country="GB"
    )
