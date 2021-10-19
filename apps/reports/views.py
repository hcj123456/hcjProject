from django.shortcuts import render
from rest_framework import viewsets
from reports.models import Reports
from reports.serializers import ReportsModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import permissions
import json
# Create your views here.


class ReportsViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportsModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        try:
            response.data['summary'] = json.loads(response.data['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return response
