from django.db import models


class Contact(models.Model):
    """Contact model for storing name, date of birth and contact information for a person."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]


class EmailAddress(models.Model):
    """Model for storing Email Addresses, linked to a contact."""

    contact = models.ForeignKey(
        Contact, related_name="email_addresses", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    email_address = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class PhoneNumber(models.Model):
    """Model for storing Phone Numbers, linked to a contact."""

    contact = models.ForeignKey(
        Contact, related_name="phone_numbers", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class PostalAddress(models.Model):
    """Model for storing Addresses."""

    contacts = models.ManyToManyField(
        Contact,
        blank=True,
        related_name="postal_addresses",
        through="PostalAddressContact",
    )
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200, null=True, blank=True)
    post_code = models.CharField(max_length=200)
    # post_code = models.RegexField(regex=r'[0-9]{4,5}|[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}')
    country = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class PostalAddressContact(models.Model):
    """Model for storing Contact to Address relationships."""

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    postal_address = models.ForeignKey(PostalAddress, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
