from rest_framework import serializers
from .models import Interfaces


class InterfaceModelSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Interfaces
        fields = '__all__'