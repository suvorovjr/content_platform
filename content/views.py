from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from datetime import datetime
from itertools import chain
from common.mixins import SlugifyMixin, TitleMixin, LoginRequiredMixin, IsAuthorMixin, AuthorRequiredMixin
from django.views import generic
from .forms import PostForm, VideoForm
from payment.models import Payment, Subscription
from .models import Post, Video


class BaseDetailView(TitleMixin, generic.DetailView):
    success_url = reverse_lazy('users:profile')

    def dispatch(self, request, *args, **kwargs):
        publication = self.get_object()
        if publication.is_paid_content:
            is_paid = Payment.objects.filter(user=request.user, author=publication.author,
                                             end_date__gt=datetime.now()).exists()
            is_author = publication.author == request.user.author if request.user.is_author else False
            if not is_paid and not is_author:
                redirect_url = f"{reverse('payment:pay_offer')}?author_id={publication.author.id}"
                return HttpResponseRedirect(redirect_url)
        return super().dispatch(request, *args, **kwargs)


class BaseCreateView(LoginRequiredMixin, SlugifyMixin, TitleMixin, generic.CreateView):
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        if form.is_valid():
            publication = form.save()
            publication.author = self.request.user.author
            publication.slug = self.get_unique_slug(publication.title)
            publication.author.save()
        return super().form_valid(form)


class BaseUpdateView(AuthorRequiredMixin, SlugifyMixin, TitleMixin, generic.UpdateView):
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        if form.is_valid():
            new_publication = form.save()
            if new_publication.title:
                new_publication.slug = self.get_unique_slug(new_publication.title)
            new_publication.author.save()
        return super().form_valid(form)


class BaseDeleteView(IsAuthorMixin, TitleMixin, AuthorRequiredMixin, generic.DeleteView):
    success_url = reverse_lazy('users:profile')


class PostCreateView(BaseCreateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    title = 'Создание поста'


class VideoCreateView(BaseCreateView):
    model = Video
    form_class = VideoForm
    template_name = 'content/video_form.html'
    title = 'Создание видео'


class PostUpdateView(IsAuthorMixin, BaseUpdateView):
    model = Post
    form_class = PostForm
    template_name = 'content/post_form.html'
    title = 'Измененние поста'


class VideoUpdateView(IsAuthorMixin, BaseUpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'content/video_form.html'
    title = 'Измененние видео'


class FeedListView(LoginRequiredMixin, TitleMixin, generic.ListView):
    template_name = 'content/feed.html'
    title = 'Лента'

    def get_queryset(self):
        user = self.request.user
        authors_ids = Subscription.objects.filter(user=user, is_active=True).values_list('author_id', flat=True)
        videos = Video.objects.filter(author_id__in=authors_ids)
        posts = Post.objects.filter(author_id__in=authors_ids)
        combined_results = list(chain(videos, posts))
        combined_results.sort(key=lambda x: x.created_at, reverse=True)
        return combined_results


class PostDetailView(BaseDetailView):
    model = Post
    title = 'Просмотр статьи'


class VideoDetailView(BaseDetailView):
    model = Video
    title = 'Просмотр видео'


class PostDeleteView(BaseDeleteView):
    model = Post


class VideoDeleteView(BaseDeleteView):
    model = Video
