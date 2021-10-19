from interfaces.models import Interfaces
from utils.common import datetime_fmt
from rest_framework import serializers
from projects.models import Projects
from testsuites.models import Testsuits
import re
from utils.validates import is_existed_env_id


def validate_include(value):
    obj = re.match(r'^\[\d+(, *\d+)+\]$', value)
    if obj is None:
        raise serializers.ValidationError("参数格式有误")
    result = obj.group()
    try:
        data = eval(result)
    except:
        raise serializers.ValidationError("参数格式有误")
    for i in data:
        if not Interfaces.objects.filter(id=i).exists():
            raise serializers.ValidationError(f"接口id【{i}】不存在")


class TestsuitsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    project_id = serializers.PrimaryKeyRelatedField(label="所属项目id", help_text="所属项目id", queryset=Projects.objects.all())

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'include', 'project', 'project_id', 'create_time', 'update_time')
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'update_time': {
                'read_only': True,
                'format': datetime_fmt()
            },
            'include': {
                'validators': [validate_include]
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['project'] = result.pop('project_id')
        return result


class TestsuitsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(write_only=True, help_text="", validators=[is_existed_env_id])

    class Meta:
        model = Testsuits
        fields = ('id', 'env_id')