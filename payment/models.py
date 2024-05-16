from django.db import models

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
