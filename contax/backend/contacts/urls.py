from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('contacts/', views.contact_list),
    path('contacts/<int:pk>', views.contact_detail),
]