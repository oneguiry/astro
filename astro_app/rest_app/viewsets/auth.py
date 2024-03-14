from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from psycopg2 import IntegrityError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.controllers.controller_user import ControllerUser
from core.models import AccountManager
from rest_app.serializers.account import LoginSerializer, RegisterSerializer, ForgotPasswordSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post']

    @swagger_auto_schema(
        operation_description="Авторизоваться",
        request_body=LoginSerializer,
        responses={
            403: "Ошибка авторизации",
            202: "Аторизация упешна"
        }
    )
    @action(methods=["post"], detail=False)
    def login(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=202)
        return Response("Не верные данные для авторизации.", status=403)

    @swagger_auto_schema(
        operation_description="Выйти из системы",
        responses={
            401: "Вы не авторизорованы",
            400: "Ошибка выхода из системы",
            202: "Выход из системы был успешен"
        }
    )
    @action(methods=["post"], detail=False)
    def logout(self, request):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return Response(status=202)
        return Response(status=404)

    @swagger_auto_schema(
        operation_description="Регистрация пользователя",
        request_body=RegisterSerializer,
        responses={
            401: "Вы не зарегестрированы",
            201: "Успешная регистрация"
        }
    )
    @action(methods=["post"], detail=False)
    def register(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:

            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        longitude = request.data.get('longitude', None)
        latitude = request.data.get('latitude', None)
        serializer = RegisterSerializer(data=request.data,
                                        context={'ip': ip, 'longitude': longitude, 'latitude': latitude})
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'user_id': user.id, 'message': "Для завершения регистрации подтвердите адрес электронной почты"},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Подтверждение регистрации",
        manual_parameters=[
            openapi.Parameter('confirmation_token', openapi.IN_QUERY, description="Токен подтверждения регистрации",
                              type=openapi.TYPE_STRING),
        ],
        responses={
            401: "Ошибка подтверждение регистрации",
            201: "Успешная регистрация"
        }
    )
    @action(methods=["get"], detail=False)
    def confirm_registration(self, request):
        data = request.query_params
        token = data.get('confirmation_token', None)
        user_profile = get_object_or_404(AccountManager, confirmation_token=token)
        user = user_profile.user
        user.is_active = True
        user.save()
        user_profile.confirmation_token = None
        user_profile.save()
        return Response({'message': 'Регистрация подтверждена'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Восстановление пароля",
        request_body=ForgotPasswordSerializer(many=False),
        responses={
            401: "Ошибка подтверждение регистрации",
            201: "Успешная регистрация"
        }
    )
    @action(methods=["post"], detail=False)
    def forgot_password(self, request):
        email = request.data['email']
        username = request.data['username']
        phone = request.data['phone']
        try:
            controller = ControllerUser().forgot_password(username, email, phone)
        except IntegrityError:
            return Response("Пользователь не найден", status=400)
        return Response({'message': 'Пароль отправлен на почту'}, status=status.HTTP_200_OK)
