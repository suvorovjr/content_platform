from django import template
from payment.models import Subscription

register = template.Library()


@register.filter(name='add_placeholder')
def add_placeholder(subject_form, placeholder):
    return subject_form.as_widget(attrs={'placeholder': placeholder})


@register.simple_tag(takes_context=True)
def user_avatar(context):
    request = context['request']
    avatar_url = None
    if request.user.is_authenticated:
        avatar_url = request.user.avatar if hasattr(request.user, 'avatar') else None
    return avatar_url


@register.filter(name='my_avatar')
def my_avatar(imagine):
    if imagine:
        return f'/media/{imagine}'
    return '/static/imagine/avatar_stub.jpeg'


@register.simple_tag()
def is_subscribed(user, author):
    return Subscription.objects.filter(user=user, author=author, is_active=True).exists


@register.filter
def is_instance(obj, type_name):
    return obj.__class__.__name__.lower() == type_name.lower()
