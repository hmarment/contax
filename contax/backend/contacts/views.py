from .models import Contact, EmailAddress, PostalAddress
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    ContactSerializer,
    EmailAddressSerializer,
    PostalAddressSerializer,
)


@api_view(["GET", "POST"])
def list_or_create_contact(request):
    """List all contacts, or create a new contact."""
    if request.method == "GET":
        snippets = Contact.objects.all()
        serializer = ContactSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_update_or_delete_contact(request, contact_id):
    """Retrieve, update or delete a contact."""
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def add_contact_email_address(request, contact_id):
    """Add a new contact email address."""
    if request.method == "POST":
        email_to_add = request.data
        email_address_to_add = email_to_add["email_address"]
        contact_email_addresses = [
            email.email_address
            for email in EmailAddress.objects.filter(contact_id=contact_id).all()
        ]
        # check if it already exists
        if email_address_to_add in contact_email_addresses:
            return Response(status=status.HTTP_204_NO_CONTENT)

        email_to_add["contact_id"] = contact_id
        serializer = EmailAddressSerializer(data=email_to_add)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def update_or_delete_contact_email_address(request, contact_id, email_id):
    """Update or delete a contact email address."""
    try:
        email_address = EmailAddress.objects.get(id=email_id)
    except EmailAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = EmailAddressSerializer(email_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        email_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def list_or_add_postal_address(request):
    """List all postal addresses, or create a new postal address."""
    if request.method == "GET":
        snippets = PostalAddress.objects.all()
        serializer = PostalAddressSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostalAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_update_or_delete_postal_address(request, postal_address_id):
    """Retrieve, update or delete a postal_address."""
    try:
        postal_address = PostalAddress.objects.get(id=postal_address_id)
    except PostalAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostalAddressSerializer(postal_address)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostalAddressSerializer(postal_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        postal_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
