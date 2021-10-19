from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from rest_framework.views import APIView

from users.models import Users
from users.serializers import RegisterSerializer
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializer


class UsernameIsExisted(APIView):
    def get(self, request, username):
        count = Users.objects.filter(username=username).count()
        one_dict = {
            'username': username,
            'count': count
        }
        return Response(one_dict)


class EmailIsExisted(APIView):
    def get(self, request, email):
        count = Users.objects.filter(email=email).count()
        one_dict = {
            'email': email,
            'count': count
        }
        return Response(one_dict)