from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from .models import Subscription
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
            subscription.is_active = False
            subscription.save()
        return redirect(reverse_lazy('users:index'))
