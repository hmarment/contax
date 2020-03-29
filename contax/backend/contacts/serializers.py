from rest_framework import serializers

from .models import (
    Contact,
    EmailAddress,
    PhoneNumber,
    PostalAddress,
    PostalAddressContact,
)


class EmailAddressSerializer(serializers.ModelSerializer):
    """Serializer for EmailAddress objects."""

    contact_id = serializers.IntegerField()

    class Meta:
        model = EmailAddress
        fields = ["id", "name", "email_address", "contact_id"]

    def create(self, validated_data):
        contact_id = validated_data.pop("contact_id")
        contact = Contact.objects.get(id=contact_id)
        return EmailAddress.objects.create(contact=contact, **validated_data)


class ContactEmailAddressSerializer(serializers.ModelSerializer):
    """Serializer for Contact EmailAddress objects."""

    class Meta:
        model = EmailAddress
        fields = ["id", "name", "email_address"]


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Serializer for PhoneNumber objects."""

    class Meta:
        model = PhoneNumber
        fields = ["id", "name", "phone_number"]


class PostalAddressContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact objects linked to a PostalAddress."""

    id = serializers.ReadOnlyField(source="contact.id")
    first_name = serializers.ReadOnlyField(source="contact.first_name")
    last_name = serializers.ReadOnlyField(source="contact.last_name")

    class Meta:
        model = PostalAddressContact
        fields = ["id", "first_name", "last_name"]


class ContactPostalAddressSerializer(serializers.ModelSerializer):
    """Serializer for PostalAddress objects linked to a Contact."""

    id = serializers.ReadOnlyField(source="postal_address.id")
    street = serializers.ReadOnlyField(source="postal_address.street")
    city = serializers.ReadOnlyField(source="postal_address.city")
    state = serializers.ReadOnlyField(source="postal_address.state")
    post_code = serializers.ReadOnlyField(source="postal_address.post_code")
    country = serializers.ReadOnlyField(source="postal_address.country")

    class Meta:
        model = PostalAddressContact
        fields = ["id", "name", "street", "city", "state", "post_code", "country"]


class PostalAddressSerializer(serializers.ModelSerializer):
    """Serializer for PostalAddress objects."""

    contacts = PostalAddressContactSerializer(
        source="postaladdresscontact_set", many=True, read_only=True
    )

    class Meta:
        model = PostalAddress
        fields = [
            "id",
            "street",
            "city",
            "state",
            "post_code",
            "country",
            "created",
            "last_updated",
            "contacts",
        ]


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact objects."""

    email_addresses = ContactEmailAddressSerializer(
        many=True, allow_null=True, required=False
    )
    phone_numbers = PhoneNumberSerializer(many=True, allow_null=True, required=False)
    postal_addresses = ContactPostalAddressSerializer(
        source="postaladdresscontact_set", many=True, read_only=True
    )

    class Meta:
        model = Contact
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "created",
            "last_updated",
            "email_addresses",
            "phone_numbers",
            "postal_addresses",
        ]

    def create(self, validated_data):
        email_addresses_data = validated_data.pop("email_addresses")
        phone_numbers_data = validated_data.pop("phone_numbers")

        contact = Contact.objects.create(**validated_data)

        for email_address_data in email_addresses_data:
            EmailAddress.objects.create(contact=contact, **email_address_data)

        for phone_number_data in phone_numbers_data:
            PhoneNumber.objects.create(contact=contact, **phone_number_data)

        # if there are any new contact address links, add them
        postal_addresses_data = self.initial_data.get("postal_addresses", list())
        for postal_address_data in postal_addresses_data:
            id = postal_address_data.get("id")
            name = postal_address_data.get("name")
            postal_address = PostalAddress.objects.get(pk=id)
            PostalAddressContact(
                contact=contact, postal_address=postal_address, name=name
            ).save()
        contact.save()
        # PostalAddress.objects.create(contact=contact, **postal_address_data)
        return contact

    def update(self, instance, validated_data):
        email_addresses_data = validated_data.pop("email_addresses")
        phone_numbers_data = validated_data.pop("phone_numbers")

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # create or update related email addresses
        instance_email_addresses = [
            email.email_address for email in instance.email_addresses.all()
        ]
        for email_address_data in email_addresses_data:
            email_address = email_address_data["email_address"]
            if email_address in instance_email_addresses:
                email = EmailAddress.objects.filter(
                    contact=instance, email_address=email_address
                )
                email.update(**email_address_data)
            else:
                EmailAddress.objects.create(contact=instance, **email_address_data)

        # create or update related phone numbers
        instance_phone_numbers = [
            number.phone_number for number in instance.phone_numbers.all()
        ]
        for phone_number_data in phone_numbers_data:
            phone_number = phone_number_data["phone_number"]
            if phone_number in instance_phone_numbers:
                number = PhoneNumber.objects.filter(
                    contact=instance, phone_number=phone_number
                )
                number.update(**phone_number_data)
            else:
                PhoneNumber.objects.create(contact=instance, **phone_number_data)

        postal_addresses_data = self.initial_data.get("postal_addresses", list())
        instance_postal_addresses = PostalAddressContact.objects.filter(
            contact_id=instance.id
        )
        for postal_address_data in postal_addresses_data:
            id = postal_address_data.get("id")
            name = postal_address_data.get("name")

            # first check whether there's already an existing entry for contact + address
            matched_addresses = [
                address
                for address in instance_postal_addresses
                if address.postal_address_id == id
            ]

            if len(matched_addresses) == 0:
                PostalAddressContact.objects.create(
                    contact=instance, postal_address_id=id, name=name
                )
            # only update if the name has changed
            if len(matched_addresses) == 1 and matched_addresses[0].name != name:
                contact_postal_address = PostalAddressContact.objects.filter(
                    contact=instance, postal_address_id=id
                )
                contact_postal_address.update(name=name)

        return instance
