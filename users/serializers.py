from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'last_login', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def validate_password(self, value: str):
        return make_password(value)


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = CustomUser
        fields = ('user', 'last_activity',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        custom_user, created = CustomUser.objects.update_or_create(user=user)
        return custom_user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
