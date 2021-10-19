from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Projects
from interfaces.models import Interfaces
from interfaces.serializers import InterfaceModelSerializer
from interfaces.models import Interfaces
from debugtalks.models import Debugtalks
from utils.validates import is_existed_env_id

# def is_contains_word(value):
#     if '花花' not in value:
#         raise serializers.ValidationError('项目名称必须包含”花花“这两个字')


class ProjectSerializer(serializers.ModelSerializer):

    # interfaces = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # interfaces = serializers.StringRelatedField(many=True)
    # interfaces = serializers.SlugRelatedField(slug_field='tester', read_only=True, many=True)
    interfaces = InterfaceModelSerializer(read_only=True, many=True)

    # name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=10, min_length=5, required=True,
    #                              validators=[UniqueValidator(Projects.objects.all(), message='项目名称不能重复')],
    #                              error_messages={
    #                                  'max_length': '项目名称最大不能超过10位',
    #                                  'min_length': '项目名称最小不能低于5位',
    #                                  'required': '项目名称不能为空'
    #                              })
    # leader = serializers.CharField(label='项目负责人', help_text='项目负责人', max_length=10, min_length=5)
    # desc = serializers.CharField(read_only=True)
    # token = serializers.CharField(write_only=True)
    class Meta:
        model = Projects
        fields = ('name', 'leader', 'desc', 'interfaces')
        extra_kwargs = {
            'name': {
                'max_length': 10,
                'min_length': 5,
                'required': True,
                'validators': [UniqueValidator(Projects.objects.all(), message='项目名称不能重复')],
                'error_messages': {
                    'max_length': '项目名称最大不能超过10位',
                    'min_length': '项目名称最小不能低于5位',
                    'required': '项目名称不能为空'
                }
            },
            'leader': {
                'max_length': 10,
                'min_length': 5
            }
        }

    def validate_name(self, value):
        if not value.endswith('项目'):
            raise serializers.ValidationError('项目名称必须要以”项目“这两个字结尾')
        return value

    def validate(self, attrs):
        pro_name = attrs.get('name')
        pro_leader = attrs.get('leader')
        if '花生' not in pro_name or '负责人' not in pro_leader:
            raise serializers.ValidationError("项目名称必须包含'花生'并且项目负责人必须包含'负责人'")
        return attrs

    # def create(self, validated_data):
    #     # validated_data.pop('token')
    #     # pro = Projects.objects.create(**validated_data)
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name')
    #     instance.leader = validated_data.get('leader')
    #     instance.save()
    #     # instance.token='1111111'
    #     return instance


class ProjectModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, label="项目名称", help_text="项目名称", min_length=5,
                                 validators=[UniqueValidator(Projects.objects.all(), message="")],
                                 error_messages={
                                     "max_length": "项目名只能小于等于10位",
                                     "min_length": "项目名不能小于5位",
                                     "required": "该字段是必填的，不能为空"
                                 })
    leader = serializers.CharField(max_length=8, label="项目负责人", help_text="项目负责人", min_length=5)
    desc = serializers.CharField(label="项目描述", help_text="项目描述", allow_null=True, allow_blank=True, default='')
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Projects
        exclude = ('update_time',)

    def create(self, validated_data):
        project = super().create(validated_data)
        Debugtalks.objects.create(project_id=project.id)
        return project


class ProjectNamesSerializer(serializers.ModelSerializer):

    # email = serializers.CharField(write_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'name')
        # exclude = ('leader',)
        # fields = '__all__'


class InterfacesNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class InterfacesSerializer(serializers.ModelSerializer):

    interfaces = InterfacesNamesSerializer(label="接口信息", help_text="接口信息", read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ('interfaces',)


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(write_only=True,validators=[is_existed_env_id])

    class Meta:
        model = Projects
        fields = ('id', 'env_id')