import uuid
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Email', **NULLABLE)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    is_author = models.BooleanField(default=False, verbose_name='Признак авторства')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    blog_name = models.CharField(max_length=35, verbose_name='Название блога')
    slug = models.CharField(max_length=50, unique=True, verbose_name='Слаг', **NULLABLE)
    blog_description = models.TextField(verbose_name='Описание блога')
    subscription_price = models.PositiveSmallIntegerField(verbose_name='Стоимость подписки',
                                                          validators=[MaxValueValidator(9999)])

    def __str__(self):
        return f'{self.blog_name} - {self.subscription_price}'

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

# class Subscription(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='subscription_to', verbose_name='Автор')
#     is_active = models.BooleanField(default=True, verbose_name='Признак подписки')
#
#     def __str__(self):
#         return f'{self.user} {"подписан" if self.is_active else "не подписан"} {self.author}'
#
#     class Meta:
#         verbose_name = 'подписка'
#         verbose_name_plural = 'подписки'
