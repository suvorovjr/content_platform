from django.shortcuts import redirect
from django.views import View
from django.conf import settings
from .models import Subscription, Payment
from .services import get_payment
from users.models import Author


class SubscribeToAuthor(View):

    def post(self, request, *args, **kwargs):
        author_id = self.request.POST.get('author_id', None)
        user = self.request.user
        author = Author.objects.get(id=author_id)
        if not Subscription.objects.filter(user=user, author=author).exists():
            Subscription.objects.create(user=request.user, author=author)
        else:
            subscription = Subscription.objects.get(user=request.user, author=author)
            if subscription.is_active:
                subscription.is_active = False
            else:
                subscription.is_active = True
            subscription.save()
        return redirect(request.META['HTTP_REFERER'])


class PaymentCreateView(View):
    def post(self, request, *args, **kwargs):
        author_id = self.request.POST.get('author_id', None)
        user = self.request.user
        author = Author.objects.get(id=author_id)
        if not Payment.objects.filter(user=user, author=author, is_paid=False).exists():
            new_payment = get_payment(settings.STRIPE_API_KEY, author)
            payment = Payment.objects.create(
                user=user,
                author=author,
                stripe_subscription_id=new_payment.get('stripe_payment_id'),
                stripe_url=new_payment.get('stripe_url')
            )
            payment.save()
        else:
            payment = Payment.objects.get(user=user, author=author, is_paid=False)
        return redirect(payment.stripe_url)
