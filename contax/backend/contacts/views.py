from .models import Contact
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer


@api_view(["GET", "POST"])
def contact_list(request):
    """
    List all contacts, or create a new contact.
    """
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
def contact_detail(request, pk):
    """
    Retrieve, update or delete a contact.
    """
    try:
        contact = Contact.objects.get(id=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
