from django.contrib import admin
from .models import Post, Video


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_paid_content', 'author')


@admin.register(Video)
class UserAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_paid_content', 'author')
