import uuid
from django.db import models
from users.models import User, Author, NULLABLE


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE, )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='subscription_to', verbose_name='Автор')
    is_active = models.BooleanField(default=True, verbose_name='Признак подписки')

    def __str__(self):
        return f'{self.user} {"подписан" if self.is_active else "не подписан"} {self.author}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='payment_to', verbose_name='Автор')
    stripe_customer_id = models.CharField(max_length=255, verbose_name='Stripe ID')
    stripe_url = models.CharField(max_length=455, verbose_name='Ссылка для оплаты')
    is_paid = models.BooleanField(default=False, verbose_name='Признак оплаты')
    end_date = models.DateField(verbose_name='Дата окончания подписки', **NULLABLE)

    def __str__(self):
        return f'{self.user} {"оплатил" if self.is_paid else "не оплатил"} подписку на{self.author}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
