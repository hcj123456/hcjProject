from rest_framework import serializers
from envs.models import Envs
from utils.common import datetime_fmt


class EnvsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            }
        }


class EnvsNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Envs
        fields = ('id', 'name')