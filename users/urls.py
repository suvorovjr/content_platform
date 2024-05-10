from django.contrib.auth.views import LogoutView
from django.urls import path
from users.apps import UsersConfig
from .views import IndexView, UserCreateView, LoginView, ConfirmCodeView, UserListView, FlagAuthorView, ProfileView, \
    ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', UserCreateView.as_view(), name='login'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('confirm_code/', ConfirmCodeView.as_view(), name='confirm_code'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('flag-autor/', FlagAuthorView.as_view(), name='flag-autor'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('blogger/list/', UserListView.as_view(), name='list'),
]
