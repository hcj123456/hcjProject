from projects.models import Projects
from interfaces.models import Interfaces
from rest_framework import serializers
from envs.models import Envs


def is_existed_project_id(value_id):
    pro = Projects.objects.filter(id=value_id)
    if not pro.exists():
        raise serializers.ValidationError("项目id不存在")


def is_existed_interface_id(value_id):
    pro = Interfaces.objects.filter(id=value_id)
    if not pro.exists():
        raise serializers.ValidationError("接口id不存在")


def is_existed_env_id(value_id):
    pro = Envs.objects.filter(id=value_id)
    if not pro.exists():
        raise serializers.ValidationError("环境配置id不存在")

