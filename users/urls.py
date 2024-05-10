from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import IndexView, UserCreateView, LoginView, ConfirmCodeView

app_name = UsersConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', UserCreateView.as_view(), name='login'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('confirm_code/', ConfirmCodeView.as_view(), name='confirm_code'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('blogger/list/', LogoutView.as_view(), name='list'),
]
