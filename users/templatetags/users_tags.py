from django import template

register = template.Library()


@register.filter(name='add_id')
def add_id(subject_form, new_id):
    return subject_form.as_widget(attrs={'id': new_id})


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
