from django.shortcuts import render
from rest_framework import viewsets
from debugtalks.models import Debugtalks
from debugtalks.serializers import DebugtalksModelSerializer
from rest_framework import permissions
from utils.pagination import PageNumberPagination
from rest_framework import filters
from rest_framework.response import Response
# Create your views here.


class DebugtalksViewSet(viewsets.ModelViewSet):
    queryset = Debugtalks.objects.all()
    serializer_class = DebugtalksModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = {
            'id': instance.id,
            'debugtalks': instance.debugtalk
        }
        return Response(data_dict)
