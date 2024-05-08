from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Email')
    confirm_code = models.CharField(max_length=6, verbose_name='Код подтверждения', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')
    is_author = models.BooleanField(default=False, verbose_name='Автор')
    subscription_price = models.PositiveSmallIntegerField(verbose_name='Стоимость подписки',
                                                          validators=[MaxValueValidator(9999)])
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
