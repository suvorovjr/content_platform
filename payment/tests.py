from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .models import Subscription
from .views import UserSubscriptionList
from users.models import User, Author


class UserSubscriptionListTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_author(self):
        request = self.factory.get('/payment/subscribers-list')
        request.user = self.user
        response = UserSubscriptionList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_with_non_author(self):
        request = self.factory.get('/payment/subscribers-list')
        request.user = AnonymousUser()
        response = UserSubscriptionList.as_view()(request)
        self.assertEqual(response.status_code, 302)

# class SubscribeToAuthorTest(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(phone_number='9876543211', password='password')
#         self.author_user = User.objects.create(phone_number='9876543210', password='password', is_author=True)
#         self.author = Author.objects.create(
#             user=self.author_user,
#             blog_name='Test blogname',
#             blog_description='Test description blog. Description for test.',
#             subscription_price=2000
#         )
#         self.client = Client()
#         self.url = reverse('payment:subscribe_author')
#
#     def test_subscribe_to_author_with_valid_author_id(self):
#         data = {'author_id': self.author.id}
#         self.client.login(username='9876543211', password='password')
#         response = self.client.post(self.url, data)
#         print(response)  # Чтобы увидеть содержимое ответа
#         print(response.status_code)
