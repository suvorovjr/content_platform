from django import template

register = template.Library()


@register.filter(name='format_phone')
def format_phone(phone_number):
    phone_number = str(phone_number)
    if len(phone_number) == 10:
        return '{}-{}-{}-{}'.format(phone_number[:3], phone_number[3:6], phone_number[6:8], phone_number[8:])
    return phone_number
