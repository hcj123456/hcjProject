from rest_framework import serializers
from debugtalks.models import Debugtalks


class DebugtalksModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField()

    class Meta:
        model = Debugtalks
        exclude = ('update_time', 'create_time')
        read_only_fields = ('name', 'project')

        extra_kwargs = {
            'debugtalk': {
                'write_only': True
            }
        }