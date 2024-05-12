from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    is_author = models.BooleanField(default=False, verbose_name='Автор')
    author_username = models.CharField(max_length=25, verbose_name='Никнейм автора', **NULLABLE)
    subscription_price = models.PositiveSmallIntegerField(verbose_name='Стоимость подписки',
                                                          validators=[MaxValueValidator(9999)], **NULLABLE)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_to')
    paid_content = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
