from rest_framework import serializers
from users.models import Users
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(help_text='用户名', label='用户名', validators=[UniqueValidator(queryset=Users.objects.all(), message='注册用户名不能重复')], max_length=20, min_length=6, error_messages={
        'required': '该字段是必填的，不能为空',
        # 'unique': '注册用户名不能重复',
        'max_length': '仅允许6-20个字符得用户名',
        'min_length': '仅允许6-20个字符得用户名'
    })
    email = serializers.EmailField(write_only=True, help_text='邮箱', label='邮箱', required=True, validators=[UniqueValidator(queryset=Users.objects.all(), message='此邮箱已注册')])
    password = serializers.CharField(help_text='用户密码', label='用户密码', max_length=20, min_length=6, write_only=True, error_messages={
        'max_length': '仅允许6-20个字符',
        'min_length': '仅允许6-20个字符'
    })
    password_confirm = serializers.CharField(help_text='确认密码', label='确认密码', max_length=20, min_length=6, write_only=True, error_messages={
        'max_length': '仅允许6-20个字符',
        'min_length': '仅允许6-20个字符'
    })
    token = serializers.CharField(label='生成token', read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'token')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('密码与确认密码不一致，请重新输入')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Users.objects.create_user(**validated_data)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user