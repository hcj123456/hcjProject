from rest_framework import serializers
from interfaces.models import Interfaces
from projects.models import Projects
from .models import Testcases
from utils import validates


class InterfacesProjectsModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    pid = serializers.IntegerField(write_only=True, label="所属项目id", help_text="所属项目id", validators=[validates.is_existed_project_id])
    iid = serializers.IntegerField(write_only=True, label="所属接口id", help_text="所属接口id", validators=[validates.is_existed_interface_id])

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        pid = attrs['pid']
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError('项目id和接口id不匹配')
        return attrs


class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesProjectsModelSerializer(label="", help_text="")

    class Meta:
        model = Testcases
        exclude = ('update_time', 'create_time')
        extra_kwargs = {
            "request": {
                "write_only": True
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.pop('interfaces').get('iid')
        result['interface_id'] = iid
        return result

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('include')
        return result


class TestcasesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[validates.is_existed_env_id])

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')