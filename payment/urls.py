from django.urls import path
from payment.apps import PaymentConfig
from .views import SubscribeToAuthor

app_name = PaymentConfig.name

urlpatterns = [
    path('subscribe-author/', SubscribeToAuthor.as_view(), name='subscribe_author'),
]
