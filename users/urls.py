from django.urls import path
from users.apps import UsersConfig
from .views import IndexView

app_name = UsersConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
