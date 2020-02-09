from rest_framework import serializers

from .models import Contact, EmailAddress, PhoneNumber, PostalAddress


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ['name', 'email_address', 'created', 'last_updated']


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['name', 'phone_number', 'created', 'last_updated']


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddress
        fields = ['name', 'street', 'city', 'state', 'post_code', 'country', 'created', 'last_updated']

class ContactSerializer(serializers.ModelSerializer):

    email_addresses = EmailAddressSerializer(many=True, allow_null=True, required=False)
    phone_numbers = PhoneNumberSerializer(many=True, allow_null=True, required=False)
    postal_addresses = PostalAddressSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'created', 'last_updated', 'email_addresses', 'phone_numbers', 'postal_addresses']

    def create(self, validated_data):
        email_addresses_data = validated_data.pop('email_addresses')
        phone_numbers_data = validated_data.pop('phone_numbers')
        postal_addresses_data = validated_data.pop('postal_addresses')

        contact = Contact.objects.create(**validated_data)
        
        for email_address_data in email_addresses_data:
            EmailAddress.objects.create(contact=contact, **email_address_data)

        for phone_number_data in phone_numbers_data:
            PhoneNumber.objects.create(contact=contact, **phone_number_data)

        for postal_address_data in postal_addresses_data:
            PostalAddress.objects.create(contact=contact, **postal_address_data)

        return contact
    
    def update(self, instance, validated_data):
        email_addresses_data = validated_data.pop('email_addresses')
        phone_numbers_data = validated_data.pop('phone_numbers')
        postal_addresses_data = validated_data.pop('postal_addresses')

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # create or update related email addresses
        instance_email_addresses = [email.email_address for email in instance.email_addresses.all()]
        for email_address_data in email_addresses_data:
            email_address = email_address_data['email_address']
            if email_address in instance_email_addresses:
                email = EmailAddress.objects.filter(contact=instance, email_address=email_address)
                email.update(**email_address_data)
            else:
                for email_address_data in email_addresses_data:
                    EmailAddress.objects.create(contact=instance, **email_address_data)

        # create or update related phone numbers
        instance_phone_numbers = [number.phone_number for number in instance.phone_numbers.all()]
        for phone_number_data in phone_numbers_data:
            phone_number = phone_number_data['phone_number']
            if phone_number in instance_phone_numbers:
                number = PhoneNumber.objects.filter(contact=instance, phone_number=phone_number)
                number.update(**phone_number_data)
            else:
                for phone_number_data in phone_numbers_data:
                    PhoneNumber.objects.create(contact=instance, **phone_number_data)

        # create or update related postal addresses
        instance_postal_addresses = [address.name for address in instance.postal_addresses.all()]
        for postal_address_data in postal_addresses_data:
            postal_address = postal_address_data['name']
            if postal_address in instance_postal_addresses:
                address = PostalAddress.objects.filter(contact=instance, name=name)
                address.update(**postal_address_data)
            else:
                for postal_address_data in postal_addresses_data:
                    PostalAddress.objects.create(contact=instance, **postal_address_data)
        
        return instance




# class EmailAddressSerializer(serializers.Serializer):

#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField(max_length=200)
#     last_name = serializers.CharField(max_length=1000)
#     date_of_birth = serializers.DateField()
#     created = serializers.DateTimeField(read_only=True)
#     last_updated = serializers.DateTimeField(read_only=True)

#     def create(self, validated_data):
#         return Contact.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance




# class EmailAddress(models.Model):
#     contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     email_address = models.EmailField()
#     created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)


# class PhoneNumber(models.Model):
#     contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)

# class PostalAddress(models.Model):
#     name = models.CharField(max_length=200)
#     street = models.CharField(max_length=200)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     post_code = models.CharField(max_length=200)
#     # post_code = models.RegexField(regex=r'[0-9]{4,5}|[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}')
#     country = models.CharField(max_length=2)
#     contacts = models.ManyToManyField(Contact)
#     created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)