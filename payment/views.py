import stripe
from common.mixins import TitleMixin, LoginRequiredMixin
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views import generic
from django.conf import settings
from .models import Subscription, Payment
from .services import get_payment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from users.models import Author


class SubscribeToAuthor(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        author_id = self.request.POST.get('author_id', None)
        user = self.request.user
        author = Author.objects.get(id=author_id)
        if user.author == author if user.is_author else None:
            return HttpResponseForbidden("Вы не можете подписаться на себя.")
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


class UserSubscriptionList(TitleMixin, LoginRequiredMixin, generic.ListView):
    model = Subscription
    title = 'Мои подписки'
    template_name = 'payment/subscription_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = Subscription.objects.filter(user=user, is_active=True)
        return queryset


class PaymentCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        author_id = self.request.POST.get('author_id', None)
        user = self.request.user
        author = Author.objects.get(id=author_id)
        if not Payment.objects.filter(user=user, author=author, is_paid=False).exists():
            new_payment = get_payment(settings.STRIPE_API_KEY, author, user)
            payment = Payment.objects.create(
                user=user,
                author=author,
                stripe_customer_id=new_payment.get('stripe_customer_id'),
                stripe_url=new_payment.get('stripe_url')
            )
            payment.save()
        else:
            payment = Payment.objects.get(user=user, author=author, is_paid=False)
        return redirect(payment.stripe_url)


class PayOfferView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'payment/pay_offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_id = self.request.GET.get('author_id')
        if author_id:
            context['author_id'] = author_id
        return context


@require_POST
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event.type == 'invoice.payment_succeeded':
        customer = event.data.object.get('customer')
        is_paid = event.data.object.get('paid')
        end_date = datetime.fromtimestamp(event.data.object.get('period_end')).date() + relativedelta(months=1)
        payment = Payment.objects.get(stripe_customer_id=customer)
        payment.end_date = end_date
        payment.is_paid = is_paid
        payment.save()
    return HttpResponse(status=200)
