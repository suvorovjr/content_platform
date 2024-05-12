from django.db import models
from users.models import User, NULLABLE


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=155, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Информациионный блок')
    imagine = models.ImageField(upload_to='post_images/', verbose_name='Облложка', **NULLABLE)
    is_paid_content = models.BooleanField(verbose_name='Флаг платной статьи')

    def __str__(self):
        return f'{self.title} - {self.is_paid_content}'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
