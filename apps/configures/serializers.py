from interfaces.models import Interfaces
from rest_framework import serializers
from configures.models import Configures
from utils.validates import is_existed_interface_id, is_existed_project_id


class InterfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label="项目名称", help_text="项目名称")
    pid = serializers.IntegerField(write_only=True, label="项目ID", help_text="项目ID", validators=[is_existed_project_id])
    iid = serializers.IntegerField(write_only=True, label="", help_text="", validators=[is_existed_interface_id])

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError("项目和接口信息不对应")
        return attrs


class ConfiguresModelSerializer(serializers.ModelSerializer):
    interface = InterfacesAnotherSerializer(label="", help_text="")

    class Meta:
        model = Configures
        fields = ('id', 'name', 'interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        iid = result.pop('interface').get('iid')
        result['interface_id'] = iid
        return result