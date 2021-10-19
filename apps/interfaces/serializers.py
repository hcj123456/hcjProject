from rest_framework import serializers
from .models import Interfaces
from projects.models import Projects
from utils import common
from testcases.models import Testcases
from configures.models import Configures
from utils.validates import is_existed_env_id


class InterfaceModelSerializer(serializers.ModelSerializer):

    # project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    project = serializers.StringRelatedField(label="所属项目名称", help_text="所属项目名称")
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label="", help_text="")

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'tester', 'create_time', 'desc', 'project', 'project_id')
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                "format": common.datetime_fmt()
            }
        }

    def to_internal_value(self, data):
        tmp = super().to_internal_value(data)
        tmp['project'] = tmp.pop('project_id')
        return tmp

    def to_representation(self, instance):
        tmp = super().to_representation(instance)
        tmp['project'] = tmp.pop('project_id')
        return tmp


class TestcasesNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
    testcases = TestcasesNamesSerializer(read_only=True, many=True)

    class Meta:
        model = Interfaces
        fields = ('testcases',)


class ConfiguresNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfaceIdModelSerializer(serializers.ModelSerializer):
    configures = ConfiguresNamesSerializer(read_only=True, many=True)

    class Meta:
        model = Interfaces
        fields = ('configures',)


class InterfaceRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(validators=[is_existed_env_id])

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')
