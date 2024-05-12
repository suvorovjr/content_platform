from django.urls import path
from .views import PostCreateView, PostUpdateView, FeedListView, PostDetailView, PostDeleteView
from .apps import ContentConfig

app_name = ContentConfig.name

urlpatterns = [
    path('blog/create/', PostCreateView.as_view(), name='blog-create'),
    path('blog/update/<int:pk>/', PostUpdateView.as_view(), name='blog-update'),
    path('blog/detail/<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
    path('blog/delete/<int:pk>', PostDeleteView.as_view(), name='blog-delete'),
    path('blog/feed/', FeedListView.as_view(), name='blog-delete'),
]
