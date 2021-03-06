from django.contrib.auth import login, logout
from django.shortcuts import render
from rest_framework import views, authentication
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.serializers import ValidationError

# from .forms import AppointmentForm

# Create your views here.
from core.serializers import *


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            # user.backend = settings.AUTHENTICATION_BACKENDS[0]
            login(request, user)

            return Response({'message': 'Login Successful'}, status=200)

        except ValidationError as e:
            return Response({'message': e.detail.get('non_field_errors')[0]}, status=401)


class RegisterView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = BlogUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': str(serializer.errors)}, status=400)
        user = serializer.create(serializer.validated_data)
        # user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)

        return Response({'message': 'Registered Successfully'}, status=200)


class LogoutView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return Response(status=200)
        return Response(status=401)


class PostView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response({'message': 'posted successfully'}, status=200)
        else:
            return Response({'message': str(serializer.errors)}, status=400)

    def put(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                post_id = request.data.get('post_id')
                if post_id:
                    post = Post.objects.get(id=request.data.get('post_id'))
                else:
                    return Response(status=400)
            except Post.DoesNotExist:
                return Response({'message': 'no such post'}, status=404)
            if request.user == post.user:
                serializer.update(post, serializer.validated_data)
                return Response({'message': 'edited successfully'}, status=200)
            else:
                return Response(status=403)
        else:
            return Response({'message': str(serializer.errors)}, status=400)

    def delete(self, request):
        try:
            post = Post.objects.get(id=request.data.get('post_id'))
        except:
            return Response({'message': 'no such post'}, status=404)
        if post.user == request.user:
            post.delete()
            return Response({'message': 'deleted successfully'}, status=200)
        else:
            return Response(status=403)


class CommentView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=False):
            serializer.create(serializer.validated_data)
            return Response({'message': 'comment sent successfully'}, status=200)
        else:
            return Response({'message': str(serializer.errors)}, status=400)

    def delete(self, request):
        try:
            comment = Comment.objects.get(id=request.data.get('comment_id'))
        except:
            return Response({'message': 'no such comment'}, status=404)
        if comment.user == request.user:
            comment.delete()
            return Response({'message': 'deleted successfully'}, status=200)
        else:
            return Response(status=403)


@api_view(['POST'])
@login_required(login_url='/api/login')
@authentication_classes([CsrfExemptSessionAuthentication])
def like_post(request):
    user = request.user
    try:
        post = Post.objects.get(id=request.POST.get('post_id'))
    except:
        return Response(status=404)
    if user in post.dislikes.all():
        post.dislikes.remove(user)
    post.likes.add(user)
    return Response(status=200)


@api_view(['POST'])
@login_required(login_url='/api/login')
@authentication_classes([CsrfExemptSessionAuthentication])
def dislike_post(request):
    user = request.user
    try:
        post = Post.objects.get(id=request.POST.get('post_id'))
    except:
        return Response(status=404)
    if user in post.likes.all():
        post.likes.remove(user)
    post.dislikes.add(user)
    return Response(status=200)


@api_view(['POST'])
@login_required(login_url='/api/login')
@authentication_classes([CsrfExemptSessionAuthentication])
def like_comment(request):
    user = request.user
    try:
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
    except:
        return Response(status=404)
    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
    comment.likes.add(user)
    return Response(status=200)


@api_view(['POST'])
@login_required(login_url='/api/login')
@authentication_classes([CsrfExemptSessionAuthentication])
def dislike_comment(request):
    user = request.user
    try:
        comment = Comment.objects.get(id=request.POST.get('comment_id'))
    except:
        return Response(status=404)
    if user in comment.likes.all():
        comment.likes.remove(user)
    comment.dislikes.add(user)
    return Response(status=200)


@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication])
def is_edited(request):
    try:
        post = Post.objects.get(id=request.GET.get('post_id'))
    except:
        return Response(status=404)
    message = True
    if post.last_edited == post.posted_time:
        message = False

    return Response({'message': message}, status=200)
