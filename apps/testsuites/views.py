import os
from datetime import datetime

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from testsuites.models import Testsuits
from testsuites.serializers import TestsuitsModelSerializer, TestsuitsRunSerializer
from testsuites.utils import get_testcases_by_interface_ids
from utils.pagination import PageNumberPagination
from rest_framework import permissions
from hcjProject import settings
from testcases.models import Testcases
from utils import common
from envs.models import Envs
# Create your views here.


class TestsuitsViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.object.all()
    serializer_class = TestsuitsModelSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)

        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        os.mkdir(testcase_dir_path)

        include = eval(instance.include)
        if len(include) == 0:
            data = {
                'ret': False,
                'msg': "此套件下未添加接口, 无法运行"
            }
            return Response(data)
        include = get_testcases_by_interface_ids(include)
        if len(include) == 0:
            data = {
                'ret': False,
                'msg': "此接口下未添加用例, 无法运行"
            }
            return Response(data)

        for testcase_id in include:
            testcase_obj = Testcases.objects.filter(id=testcase_id).first()
            if testcase_obj:
                common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

        return common.generate_report(instance, testcase_dir_path)


    def get_serializer_class(self):
        if self.action == 'run':
            return TestsuitsRunSerializer
        else:
            return self.serializer_class