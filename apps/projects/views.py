from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from django.db import connection
from rest_framework.generics import GenericAPIView

from .models import Projects
from interfaces.models import Interfaces
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework import mixins
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

import json
from projects.serializers import ProjectSerializer,ProjectNameSerializer,InterfacesSerializer
from utils.pagination import PageNumberPagination


# Create your views here.


# class ProjectViewSet(GenericAPIView):
# class ProjectViewSet(mixins.DestroyModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      GenericAPIView):
# class ProjectViewSet(generics.ListAPIView,
#                      generics.CreateAPIView,
#                      generics.RetrieveAPIView,
#                      generics.UpdateAPIView,
#                      generics.DestroyAPIView):
class ProjectViewSet(viewsets.ModelViewSet):

    # def get_object(self, id):
    #     # ret = {
    #     #     'msg': '参数异常',
    #     #     'code': 0
    #     # }
    #     try:
    #         return Projects.objects.get(id=id)
    #     except Exception:
    #         # return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #         raise Http404

    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    search_fields = ['name', 'leader']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', '-leader']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    @action(methods=['GET', 'POST'], detail=False)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # names_list = []
        # for i in queryset:
        #     names_list.append({
        #         '项目名称': i.name
        #     })
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        # pro = self.get_object()
        # serializer = self.get_serializer(instance=pro)
        pro = self.retrieve(request, *args, **kwargs)
        pro.data = pro.data.get('interfaces')
        return Response(pro.data)

    # @action(methods=['GET'], detail=True)
    # def projects(self, request, *args, **kwargs):
    #     pro = self.get_object()
    #     serializer = self.get_serializer(instance=pro)
    #     return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'names':
            return ProjectNameSerializer
        elif self.action == 'interfaces':
            return InterfacesSerializer
        else:
            return self.serializer_class

    # def get_queryset(self):
    #     if self.action == 'projects':
    #         return Interfaces.objects.all()
    #     else:
    #         return self.queryset
    # lookup_field = 'id'

    # def get(self, request, *args, **kwargs):
    # #     # one_project = Projects(name='hcj项目1', leader='hcj负责人', desc='hcj描述')
    # #     # one_project.save()name='hcj项目1', leader='hcj负责人', desc='hcj描述'
    # #     # one_project = Projects.objects.create(name='ert项目4', leader='kfd负责人rdb', desc='没空决描述swq')
    # #     # # one_list = []
    # #     # # for obj in one_project:
    # #     # #     one_dict = {
    # #     # #         'name': obj.name,
    # #     # #         'leader': obj.leader
    # #     # #     }
    # #     # #     one_list.append(one_dict)
    # #     # one_dict = {
    # #     #     'name': one_project.name,
    # #     #     'leader': one_project.leader
    # #     # }
    # #     # return JsonResponse(one_dict, json_dumps_params={"ensure_ascii": False})
    # #     # one_project = Projects.objects.filter(name__contains='2')
    # #     # one_project = Projects.objects.filter(name__startswith='A')
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.filter(name__contains='项目').filter(desc__contains='解决')
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.filter(Q(name__contains='n') | Q(desc__endswith='1'))
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.filter(interfaces__tester='hcj测试人1')
    # #     # one_project = Projects.objects.filter(interfaces__tester__contains='测试')
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.filter(name__contains='Acj')
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.interfaces.objects.filter(),
    # #     #         'tester': obj.interfaces.tester
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Interfaces.objects.filter(project_id=1)
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'tester': obj.tester
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Interfaces.objects.all()
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'tester': obj.tester
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.get(id=1)
    # #     # # one_list = []
    # #     # # for obj in one_project:
    # #     # #     one_dict = {
    # #     # #         'name': obj.name,
    # #     # #         'tester': obj.tester
    # #     # #     }
    # #     # #     one_list.append(one_dict)
    # #     # one_project.leader = '你好帅哦！哦哦'
    # #     # one_project.save()
    # #     # one_dict = {
    # #     #         'name': one_project.name,
    # #     #         'leader': one_project.leader
    # #     #     }
    # #     # return JsonResponse(one_dict, json_dumps_params={"ensure_ascii": False})
    # #     # one_project = Projects.objects.filter(Q(name__contains='1') | Q(name__contains='2')).update(leader='讨厌！')
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # one_project = Projects.objects.get(id=3)
    # #     # one_project.delete()
    # #     # one_project = Projects.objects.all().order_by('name', '-leader')
    # #     # one_project = Projects.objects.filter(id=1)
    # #     # one_list = []
    # #     # for obj in one_project:
    # #     #     one_dict = {
    # #     #         'name': obj.name,
    # #     #         'leader': obj.leader
    # #     #     }
    # #     #     one_list.append(one_dict)
    # #     # return JsonResponse(one_list, safe=False, json_dumps_params={"ensure_ascii": False})
    # #     # 1、获取所有项目数据，将获取的数据返回前端
    #     # 请求方法：GET、url路径：/projects/、返回数据：json数据
    #     """
    #     查询所有的项目数据
    #     请求方法：GET
    #     url路径：/projects/
    #     返回数据：json数据
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     return super().list(request, *args, **kwargs)
    #     # one_project = Projects.objects.all()
    #     # qs = self.queryset
    #     # qs = self.get_queryset()
    #     # queryset = self.filter_queryset(self.get_queryset())
    #     # page = self.paginate_queryset(queryset)
    #     # # pro = self.get_object()
    #     # if page is not None:
    #     #     serializer_project = self.get_serializer(instance=page, many=True)
    #     #     return self.get_paginated_response(serializer_project.data)
    #     #
    #     # serializer_project = self.get_serializer(instance=queryset, many=True)
    #     # # serializer_project = ProjectSerializer(instance=pro, many=True)
    #     # # one_list = []
    #     # # for i in one_project:
    #     # #     one_dict = {
    #     # #         'name': i.name,
    #     # #         'leader': i.leader
    #     # #     }
    #     # #     one_list.append(one_dict)
    #     # return Response(serializer_project.data, status=status.HTTP_200_OK, content_type='application/json')
    #
    # def post(self, request, *args, **kwargs):
    #     # one_project = Projects(name='hcj项目1', leader='hcj负责人', desc='hcj描述')
    #     # one_project.save()name='hcj项目1', leader='hcj负责人', desc='hcj描述'
    #     # one_project = Projects.objects.create(name='ert项目4', leader='kfd负责人rdb', desc='没空决描述swq')
    #     # # one_list = []
    #     # # for obj in one_project:
    #     # #     one_dict = {
    #     # #         'name': obj.name,
    #     # #         'leader': obj.leader
    #     # #     }
    #     # #     one_list.append(one_dict)
    #     # one_dict = {
    #     #     'name': one_project.name,
    #     #     'leader': one_project.leader
    #     # }
    #     # return JsonResponse(one_dict, json_dumps_params={"ensure_ascii": False})
    #     # one_project = Projects.objects.filter(name__contains='2')
    #     # one_project = Projects.objects.filter(name__startswith='A')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.filter(name__contains='项目').filter(desc__contains='解决')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.filter(Q(name__contains='n') | Q(desc__endswith='1'))
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.filter(interfaces__tester='hcj测试人1')
    #     # one_project = Projects.objects.filter(interfaces__tester__contains='测试')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.filter(name__contains='Acj')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.interfaces.objects.filter(),
    #     #         'tester': obj.interfaces.tester
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Interfaces.objects.filter(project_id=1)
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'tester': obj.tester
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Interfaces.objects.all()
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'tester': obj.tester
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.get(id=1)
    #     # # one_list = []
    #     # # for obj in one_project:
    #     # #     one_dict = {
    #     # #         'name': obj.name,
    #     # #         'tester': obj.tester
    #     # #     }
    #     # #     one_list.append(one_dict)
    #     # one_project.leader = '你好帅哦！哦哦'
    #     # one_project.save()
    #     # one_dict = {
    #     #         'name': one_project.name,
    #     #         'leader': one_project.leader
    #     #     }
    #     # return JsonResponse(one_dict, json_dumps_params={"ensure_ascii": False})
    #     # one_project = Projects.objects.filter(Q(name__contains='1') | Q(name__contains='2')).update(leader='讨厌！')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # one_project = Projects.objects.get(id=3)
    #     # one_project.delete()
    #     # data = request.body.decode('utf-8')
    #     # data_dict = json.loads(data)
    #     # one_project = Projects.objects.all().order_by('name', '-leader')
    #     # one_list = []
    #     # for obj in one_project:
    #     #     one_dict = {
    #     #         'name': obj.name,
    #     #         'leader': obj.leader
    #     #     }
    #     #     one_list.append(one_dict)
    #     # return JsonResponse(one_list, safe=False, json_dumps_params={"ensure_ascii": False})
    #     # one_dict = {
    #     #     "name": "没开门",
    #     #     "age": 18,
    #     #     "sex": "男"
    #     # }
    #     # json_dict = json.dumps(one_dict, ensure_ascii=False)
    #     # return HttpResponse(json_dict, content_type='application/json')
    #
    #     """
    #     创建一条项目数据
    #     请求方法：POST
    #     url路径：/projects/
    #     返回数据：json对象
    #     """
    #     return super().create(request, *args, **kwargs)
    #     # ret = {
    #     #     'msg': '参数异常',
    #     #     'code': 0
    #     # }
    #     # # data = request.body.decode('utf-8')
    #     # # try:
    #     # #     json_data = json.loads(data)
    #     # # except json.JSONDecodeError:
    #     # #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # serializer_obj = self.get_serializer(data=request.data)
    #     # try:
    #     #     serializer_obj.is_valid(raise_exception=True)
    #     # except:
    #     #     ret.update(serializer_obj.errors)
    #     #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # # one_project = Projects.objects.create(**serializer_obj.validated_data)
    #     # # one_dict = {
    #     # #     'name': one_project.name,
    #     # #     'leader': one_project.leader
    #     # # }
    #     # serializer_obj.save()
    #     # # serializer_obj1 = ProjectSerializer(instance=one_project)
    #     # return Response(serializer_obj.data)
    #
    # def delete(self, request, *args, **kwargs):
    #     """
    #     删除项目数据
    #     请求方法：DELETE
    #     url路径：/projects/id/
    #     返回数据：字符串
    #     :param id:
    #     :return:
    #     """
    #     return super().destroy(request, *args, **kwargs)
    #     # ret = {
    #     #     'msg': '参数异常',
    #     #     'code': 0
    #     # }
    #     # try:
    #     #     one_project = Projects.objects.get(id=id)
    #     # except Exception:
    #     #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # pro = self.get_object()
    #     # pro.delete()
    #     # return Response(None)
    #
    # def put(self, request, *args, **kwargs):
    #     """
    #     更新一条项目数据
    #     请求方法：POST
    #     url路径：/projects/id/
    #     返回数据： json对象
    #     :return:
    #     """
    #     return super().update(request, *args, **kwargs)
    #     # ret = {
    #     #     'msg': '参数异常',
    #     #     'code': 0
    #     # }
    #     # # try:
    #     # #     one_project = Projects.objects.get(id=id)
    #     # # except Exception:
    #     # #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # pro = self.get_object()
    #     # # try:
    #     # #     data = request.body.decode('utf-8')
    #     # #     python_data = json.loads(data)
    #     # # except json.JSONDecodeError:
    #     # #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # serializer_obj = self.get_serializer(instance=pro, data=request.data)
    #     # try:
    #     #     serializer_obj.is_valid(raise_exception=True)
    #     # except:
    #     #     ret.update(serializer_obj.errors)
    #     #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     # # pro.name = serializer_obj.validated_data.get('name')
    #     # # pro.leader = serializer_obj.validated_data.get('leader')
    #     # # pro.save()
    #     # # one_project.name='你好呀小帅哥'
    #     # serializer_obj.save()
    #     # # serializer_obj1 = ProjectSerializer(instance=pro)
    #     # return Response(serializer_obj.data)
    #
    # def get(self, request, *args, **kwargs):
    #     """
    #     获取一条项目信息
    #     :param request:
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     return super().retrieve(request, *args, **kwargs)
        # # one_project = Projects.objects.get(id=id)
        # pro = self.get_object()
        # # one_list = []
        # # for i in one_project:
        # #     # one_dict = {
        # #     #     'name': i.name,
        # #     #     'leader': i.leader
        # #     # }
        # #     one_list.append(one_dict)
        # serializer_obj = self.get_serializer(instance=pro)
        # # one_dict = {
        # #     'name': pro.name,
        # #     'leader': pro.leader
        # # }
        # return Response(serializer_obj.data)


# class ProjectViewSet1(View):
#     """
#     获取一条项目数据
#     请求方法：GET
#     url路径：/projects/id/
#     返回数据：json对象
#     """
#
#     def get_object(self, id):
#         try:
#             return Projects.objects.get(id=id)
#         except Exception:
#             raise Http404
#
#     def get(self, request, id):
#         # one_project = Projects.objects.get(id=id)
#         pro = self.get_object(id=id)
#         # one_list = []
#         # for i in one_project:
#         #     # one_dict = {
#         #     #     'name': i.name,
#         #     #     'leader': i.leader
#         #     # }
#         #     one_list.append(one_dict)
#         serializer_obj = ProjectSerializer(instance=pro)
#         # one_dict = {
#         #     'name': pro.name,
#         #     'leader': pro.leader
#         # }
#         return JsonResponse(serializer_obj.data, json_dumps_params={'ensure_ascii': False})

    # def put(self, request, id):
    #     """
    #     更新一条项目数据
    #     请求方法：POST
    #     url路径：/projects/id/
    #     返回数据： json对象
    #     :return:
    #     """
    #     ret = {
    #         'msg': '参数异常',
    #         'code': 0
    #     }
    #     # try:
    #     #     one_project = Projects.objects.get(id=id)
    #     # except Exception:
    #     #     return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     pro = self.get_object(id=id)
    #     try:
    #         data = request.body.decode('utf-8')
    #         python_data = json.loads(data)
    #     except json.JSONDecodeError:
    #         return JsonResponse(ret, status=400, json_dumps_params={'ensure_ascii': False})
    #     pro.name = python_data.get('name')
    #     pro.leader = python_data.get('leader')
    #     pro.save()
    #     # one_project.name='你好呀小帅哥'
    #     # one_project.save()
    #     one_dict = {
    #         'name': pro.name,
    #         'leader': pro.leader
    #     }
    #     return JsonResponse(one_dict, json_dumps_params={'ensure_ascii': False})
