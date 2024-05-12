from django.urls import path
from .views import PostCreateView, PostUpdateView, FeedListView, PostDetailView, PostDeleteView
from .views import VideoCreateView
from .apps import ContentConfig

app_name = ContentConfig.name

urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('video/create/', VideoCreateView.as_view(), name='video-create'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/delete/<int:pk>', PostDeleteView.as_view(), name='post-delete'),
    path('post/feed/', FeedListView.as_view(), name='post-delete'),
]
