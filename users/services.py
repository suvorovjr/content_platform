import random
import requests
from django.conf import settings


def get_confirm_code():
    confirm_code = random.randint(100000, 999999)
    return confirm_code


def send_sms_code(phone_number, confirm_code):
    sms_ru_api = settings.SMS_RU_API
    message = '+'.join(f'Ваш код подтверждения на content.ru: {confirm_code}'.split())
    requests.get(
        url=f'https://sms.ru/sms/send?api_id={sms_ru_api}&to=+7{phone_number}&msg={message}&json=1'
    )
