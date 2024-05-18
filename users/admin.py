from django.contrib import admin
from .models import User, Author


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog_name', 'subscription_price')
