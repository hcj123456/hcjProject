from django.shortcuts import render
from rest_framework import viewsets
from configures.models import Configures
from configures.serializers import ConfiguresModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import filters
from interfaces.models import Interfaces
from rest_framework.response import Response
from utils import handle_datas
import json
# Create your views here.


class ConfiguresViewSet(viewsets.ModelViewSet):
    queryset = Configures.objects.all()
    serializer_class = ConfiguresModelSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request, encoding='utf-8')

        #处理请求数据
        config_headers = config_request['config']['request'].get('headers')
        config_headers_list = handle_datas.handle_data4(config_headers)

        #处理全局变量
        config_variables = config_request['config'].get('variables')
        config_variables_list = handle_datas.handle_data2(config_variables)

        config_name = config_request['config']['name']
        selected_interface_id = config_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        datas = {
            "author": config_obj.author,
            "configure_name": config_name,
            "selected_interface_id": selected_interface_id,
            "selected_project_id":selected_project_id,
            "header": config_headers_list,
            "globalVar": config_variables_list
        }
        return Response(datas)