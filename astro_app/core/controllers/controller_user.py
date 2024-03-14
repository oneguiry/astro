from datetime import datetime
from random import choice

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from core.models import AccountManager


class ControllerUser:
    def __init__(self, pk: int = None):
        self.account = None
        if pk:
            self.account = AccountManager.objects.get(id=pk)

    @staticmethod
    def generate_password(length: int = 10):
        choice_random_select = "qwertyuiop[]asdfghjkl;zxcvbnm,./1234567890-=!@#$%^&*()_+?QWERTYUIOP{}ASDFGHJKL:|ZXCVBNM<>"
        password = "".join([choice(choice_random_select) for _ in range(length)])
        return password

    def create_user(self, username: str, name: str, email: str, password: str, surname: str,
                    date_birth: datetime, phone: str, subscription_info: bool):
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
            user.is_active = False
            self.account = AccountManager.objects.create(user=user, name=name, surname=surname, date_birth=date_birth,
                                                         phone=phone, subscription_info=subscription_info)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = False
            user.save()
            return self.account

    def deactivate(self):
        self.account.user.is_active = False
        self.account.save()

    def activate(self):
        self.account.user.is_active = True
        self.account.save()

    def forgot_password(self, username: str, email: str, phone: str):
        try:
            account = AccountManager.objects.get(user__username=username, user__email=email, phone=phone)
        except AccountManager.DoesNotExist:
            raise ValidationError("Пользователь с такими данными не существует")
        finally:
            self.account = AccountManager.objects.get(user__username=username, user__email=email, phone=phone)
            updated_password = self.generate_password()
            self.account.user.set_password(updated_password)
            self.account.save()
            subject = 'Восстановление пароля'
            message = (f'Ваш пароль был успешно сброшен. Для доступа к аккаунту Вам обновили пароль.\n'
                       f'Используйте следующий пароль для доступа к аккаунту: {updated_password}\n')
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['azimovin01@yandex.ru'], fail_silently=False)


def create_super_user():
    try:
        user = User.objects.get(username="admin")
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin', 'admin@mail.ru', '1')
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
    return user
