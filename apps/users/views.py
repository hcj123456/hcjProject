from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from users.models import Users
from users.serializers import RegisterSerializer


class UserView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer
