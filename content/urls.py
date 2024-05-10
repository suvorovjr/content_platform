from django.urls import path
from .views import PostCreateView
from .apps import ContentConfig

app_name = ContentConfig.name

urlpatterns = [
    path('blog/create/', PostCreateView.as_view(), name='blog-create'),
]
