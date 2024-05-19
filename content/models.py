import uuid
from django.db import models
from users.models import Author, NULLABLE


class AbstractPublication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=255, unique=True, verbose_name='Слаг', **NULLABLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=155, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Информациионный блок')
    video = models.FileField(upload_to='videos/', verbose_name='Видео')
    imagine = models.ImageField(upload_to='post_images/', verbose_name='Облложка', **NULLABLE)
    is_paid_content = models.BooleanField(verbose_name='Флаг платной статьи')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.is_paid_content}'

    class Meta:
        abstract = True


class Post(AbstractPublication):
    video = None

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Video(AbstractPublication):
    body = models.TextField(verbose_name='Описание видео')

    class Meta:
        verbose_name = 'видео'
        verbose_name_plural = 'видео'
