from django.contrib.auth.models import User
from django.db import models


class AccountManager(models.Model):
    name = models.CharField(u'Имя', max_length=30, null=False, blank=False)
    surname = models.CharField(u'Фамилия', max_length=30, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(u'Номер телефона', max_length=12, null=False, blank=False, unique=True)
    date_birth = models.DateField(u'Дата рождения', null=False, blank=False)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)
    profile_image = models.ImageField(upload_to='media')
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    subscription_info = models.BooleanField(u'Подписка на уведомления', default=True, null=True, blank=True)


class ModelTest(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    surname = models.CharField(max_length=30, null=False, blank=False)