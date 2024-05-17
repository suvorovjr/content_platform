from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from common.mixins import SlugifyMixin, TitleMixin
from django.views import generic
from .forms import PostForm, VideoForm
from payment.models import Subscription
from .models import Post, Video


# class IsAdminOrUserMixin(UserPassesTestMixin):
#     def test_func(self):
#         object = self.get_object()
#         return self.request.user == object.author or self.request.user.is_superuser


class BaseCreateView(SlugifyMixin, TitleMixin, generic.CreateView):
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        if form.is_valid():
            publication = form.save()
            publication.author = self.request.user.author
            publication.slug = self.get_unique_slug(publication.title)
            publication.author.save()
        return super().form_valid(form)


class PostCreateView(BaseCreateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    title = 'Создание поста'
    success_url = reverse_lazy('users:profile')


class VideoCreateView(BaseCreateView):
    model = Video
    form_class = VideoForm
    template_name = 'content/video_form.html'
    title = 'Создание видео'
    success_url = reverse_lazy('users:profile')


class PostUpdateView(TitleMixin, generic.UpdateView):
    form_class = PostForm
    success_url = reverse_lazy('users:profile')
    title = 'Измененние поста'


class VideoUpdateView(TitleMixin, generic.UpdateView):
    form_class = VideoForm
    success_url = reverse_lazy('users:profile')
    title = 'Измененние видео'


class FeedListView(generic.ListView):
    template_name = 'content/feed.html'

    def get_queryset(self):
        user = self.request.user
        authors_ids = Subscription.objects.filter(user=user, is_active=True).values_list('author_id', flat=True)
        videos = Video.objects.filter(author_id__in=authors_ids)
        posts = Post.objects.filter(author_id__in=authors_ids)
        combined_queryset = videos | posts
        combined_queryset = combined_queryset.order_by('-published_date')
        return combined_queryset


class PostDetailView(TitleMixin, generic.DetailView):
    model = Post
    title = 'Просмотр статьи'


class VideoDetailView(TitleMixin, generic.DetailView):
    model = Video
    title = 'Просмотр видео'


class PostDeleteView(generic.DeleteView):
    pass


class VideoDeleteView(generic.DeleteView):
    pass
