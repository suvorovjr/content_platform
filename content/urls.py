from django.urls import path
from .views import PostCreateView, PostUpdateView, FeedListView, PostDetailView, PostDeleteView
from .views import VideoCreateView, VideoUpdateView, VideoDetailView, VideoDeleteView, FeedListView
from .apps import ContentConfig

app_name = ContentConfig.name

urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('video/create/', VideoCreateView.as_view(), name='video-create'),
    path('post/update/<slug:slug>/', PostUpdateView.as_view(), name='post-update'),
    path('video/update/<slug:slug>/', VideoUpdateView.as_view(), name='video-update'),
    path('post/detail/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('video/detail/<slug:slug>/', VideoDetailView.as_view(), name='video-detail'),
    path('post/delete/<slug:slug>', PostDeleteView.as_view(), name='post-delete'),
    path('feed/', FeedListView.as_view(), name='feed'),
]
