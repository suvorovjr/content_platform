from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from .models import User, Author
from .views import UserCreateView, LoginView, ProfileView, AuthorProfileView, AuthorProfileUpdateView


class UserCreateViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/login')
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            UserCreateView.as_view()(request)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/login')
        request.user = AnonymousUser()
        response = UserCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/signin')
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            LoginView.as_view()(request)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/signin')
        request.user = AnonymousUser()
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/profile')
        request.user = self.user
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/profile')
        request.user = AnonymousUser()
        response = ProfileView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class AuthorProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')
        self.author_user = User.objects.create(phone_number='987654311', is_author=True)
        self.author = Author.objects.create(
            user=self.author_user,
            blog_name='Test blogname',
            blog_description='Test description blog. Description for test.',
            subscription_price=2000
        )

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/author-profile')
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            AuthorProfileView.as_view()(request)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/author-profile')
        request.user = self.author_user
        response = AuthorProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class AuthorProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(phone_number='987654310')
        self.author_user = User.objects.create(phone_number='987654311', is_author=True)
        self.author = Author.objects.create(
            user=self.author_user,
            blog_name='Test blogname',
            blog_description='Test description blog. Description for test.',
            subscription_price=2000
        )

    def test_view_with_authenticated_user(self):
        request = self.factory.get('/author-profile/update')
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            AuthorProfileUpdateView.as_view()(request)

    def test_view_with_non_authenticated_user(self):
        request = self.factory.get('/author-profile/update')
        request.user = self.author_user
        response = AuthorProfileUpdateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
