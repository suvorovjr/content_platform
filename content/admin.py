from django.contrib import admin
from .models import Post


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_paid_content')
