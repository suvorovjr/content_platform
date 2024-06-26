from django.urls import path
from payment.apps import PaymentConfig
from .views import SubscribeToAuthor, PaymentCreateView, webhook, PayOfferView, UserSubscriptionList

app_name = PaymentConfig.name

urlpatterns = [
    path('subscribe-author/', SubscribeToAuthor.as_view(), name='subscribe_author'),
    path('subscribers-list/', UserSubscriptionList.as_view(), name='subscribers_list'),
    path('pay/', PaymentCreateView.as_view(), name='pay'),
    path('offer/', PayOfferView.as_view(), name='pay_offer'),
    path('webhook/', webhook, name='webhook'),
]
