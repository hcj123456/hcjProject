import os
from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets, permissions
from interfaces.models import Interfaces
from interfaces.serializers import InterfaceModelSerializer, TestcasesByInterfaceIdModelSerializer, ConfiguresByInterfaceIdModelSerializer, InterfaceRunSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from testcases.models import Testcases
from configures.models import Configures
from envs.models import Envs
from hcjProject import settings
from utils import common
from utils.pagination import PageNumberPagination
from rest_framework import filters
# Create your views here.





class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = InterfaceModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "name"]
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for i in results:
            interface_id = i['id']
            testcases_count = Testcases.objects.filter(interface_id=interface_id).count()
            configure_count = Configures.objects.filter(interface_id=interface_id).count()
            i['testcases_count'] = testcases_count
            i['configure_count'] = configure_count
        return response

    @action(methods=['GET'], detail=True)
    def testcases(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data['testcases']
        return Response(response.data)

    @action(methods=['GET'], detail=True)
    def configures(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = response.data['configures']
        return Response(response.data)

    @action(methods=["post"], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        os.mkdir(testcase_dir_path)

        testcase_qa = Testcases.objects.filter(interface=instance)
        if not testcase_qa.exists():
            data = {
                'ret': False,
                'msg': '此接口下无用例, 无法运行'
            }
            return Response(data)

        for testcase_obj in testcase_qa:
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        return common.run_testcase(instance, testcase_dir_path)


    def get_serializer_class(self):
        if self.action == 'testcases':
            return TestcasesByInterfaceIdModelSerializer
        elif self.action == 'configures':
            return ConfiguresByInterfaceIdModelSerializer
        elif self.action == 'run':
            return InterfaceRunSerializer
        else:
            return self.serializer_class
