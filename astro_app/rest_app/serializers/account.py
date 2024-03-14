import secrets
from datetime import date

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.controllers.controller_user import ControllerUser
from core.models import AccountManager


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountManager
        fields = ['confirmation_token']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    name = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    subscription_info = serializers.BooleanField(default=True)
    date_birth = serializers.DateField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},  # Указывает тип поля ввода HTML
        min_length=8,  # Минимальная длина пароля
        max_length=32,  # Максимальная длина пароля
        allow_blank=False,  # Запретить пустые пароли
        trim_whitespace=True,  # Удалять лишние пробелы из пароля
        help_text='Ваш пароль должен содержать не менее 8 символов',  # Помощь для API документации
        error_messages={
            'min_length': 'Ваш пароль должен быть больше {min_length} символов.',
            'max_length': 'Ваш пароль должен быть меньше {max_length} символов.',
        })

    def validate_phone(self, validated_data):
        phone = validated_data.strip()
        if len(phone) != 12 and ((phone[0] == '+' and phone[1] == '7') or phone[0] == '8'):
            raise serializers.ValidationError("Ваш номер не соответствует требованиям")
        if AccountManager.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Данный номер уже используется")
        return validated_data

    def validate_username(self, validated_data):
        if AccountManager.objects.filter(user__username=validated_data).exists():
            raise ValidationError('Такой пользователь уже существует.')
        return validated_data

    def validate_email(self, validated_data):
        if AccountManager.objects.filter(user__email=validated_data).exists():
            raise ValidationError('Данный электронный адрес уже используется')
        return validated_data

    def create(self, validated_data):
        controller = ControllerUser()
        new_user = controller.create_user(**validated_data)
        confirmation_token = self._generate_random_token()
        new_user.confirmation_token = confirmation_token
        new_user.save()

        subject = 'Подтверждение регистрации'
        message = f'Для подтверждения регистрации перейдите по ссылке: {settings.BASE_URL}/auth/simple/confirm_registration?confirmation_token={confirmation_token}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.user.email])

        return new_user

    def _generate_random_token(self, length=32):
        return secrets.token_hex(length)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, max_length=12)
