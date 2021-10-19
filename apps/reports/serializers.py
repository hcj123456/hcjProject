from rest_framework import serializers
from reports.models import Reports
from utils.common import datetime_fmt


class ReportsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'read_only': True,
                'format': datetime_fmt()
            }
        }

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if res['result']:
            res['result'] = "Pass"
        else:
            res['result'] = "Fail"
        return res