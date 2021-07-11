from django.contrib.auth import authenticate
from django.forms import PasswordInput
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import *


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

    def create(self, validated_data):
        user = BlogUser.objects.create_user(username=validated_data.pop('username'),
                                            password=validated_data.pop('password'), **validated_data)
        return user


class CommentSerializer(serializers.ModelSerializer):
    required_fields = []

    class Meta:
        model = Comment
        fields = ('post', 'parent_comment', 'text')

    # def validate(self, attrs):
    #     if len(Post.objects.filter(id=attrs.get('post'))) == 0:
    #         raise ValidationError('No Such Post')
    #     elif len(Comment.objects.filter(id=attrs.get('parent_comment'))) == 0:
    #         return attrs

    def create(self, validated_data):
        comment = Comment.objects.create(user=self.context.get('request').user, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text',)

    def create(self, validated_data):
        post = Post.objects.create(user=self.context.get('request').user, text=validated_data.get('text'))
        return post

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text')
        instance.save()
        return instance
