from rest_framework import serializers

from .models import Contact, EmailAddress

class ContactSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=1000)
    date_of_birth = serializers.DateField()
    email_addresses = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True)
    created = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
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