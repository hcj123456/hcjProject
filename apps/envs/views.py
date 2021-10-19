from django.shortcuts import render
from envs.models import Envs
from envs.serializers import EnvsNamesSerializer, EnvsModelSerializer
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.pagination import PageNumberPagination
# Create your views here.


class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'names':
            return EnvsNamesSerializer
        else:
            return self.serializer_class