from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from .views import PostCreateView, FeedListView
from users.models import User


class PostCreateViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')
        self.author_user = User.objects.create(phone_number='987654311', is_author=True)

    def test_view_with_author(self):
        request = self.factory.get('/content/post/create')
        request.user = self.author_user
        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_with_non_author(self):
        request = self.factory.get('/content/post/create')
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            PostCreateView.as_view()(request)


class FeedListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/content/feed/')
        request.user = self.user
        response = FeedListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/content/feed/')
        request.user = AnonymousUser()
        response = FeedListView.as_view()(request)
        self.assertEqual(response.status_code, 302)
