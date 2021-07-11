from django.contrib.auth import login, logout
from django.shortcuts import render
from rest_framework import views, authentication
from rest_framework.response import Response
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
            return Response({'message': e.detail.get('non_field_errors')[0]})


class RegisterView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        serializer = BlogUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'message': 'Bad Credentials'}, status=400)
        user = serializer.create(serializer.validated_data)
        # user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)

        return Response({'message': 'Registered Successfully'}, status=200)


class LogoutView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            logout(user)
            return Response(status=200)
        return Response(status=401)


class PostView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pass


class CommentView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pass
