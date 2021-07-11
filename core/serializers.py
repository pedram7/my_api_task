from django.contrib.auth import authenticate
from django.forms import PasswordInput
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import BlogUser, Comment

Comment


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}
                                     , write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return user


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'biography']


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('post', 'parent_comment', 'text', 'user')

    def create(self, validated_data):
        pass


class PostSerializer(serializers.ModelSerializer):
    parent_comment = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('username', 'post', '', 'text',)
