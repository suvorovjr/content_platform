from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from .views import UserSubscriptionList
from users.models import User


class UserSubscriptionListTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_author(self):
        request = self.factory.get('/content/post/create')
        request.user = self.user
        response = UserSubscriptionList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_with_non_author(self):
        request = self.factory.get('/content/post/create')
        request.user = AnonymousUser()
        response = UserSubscriptionList.as_view()(request)
        self.assertEqual(response.status_code, 302)
