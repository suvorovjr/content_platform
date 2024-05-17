from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from itertools import chain
from common.mixins import SlugifyMixin, TitleMixin
from django.views import generic
from .forms import PostForm, VideoForm
from payment.models import Payment, Subscription
from .models import Post, Video


class BaseDetailView(generic.DetailView):

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


class FeedListView(TitleMixin, generic.ListView):
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


class PostDetailView(TitleMixin, BaseDetailView):
    model = Post
    title = 'Просмотр статьи'


class VideoDetailView(TitleMixin, BaseDetailView):
    model = Video
    title = 'Просмотр видео'


class PostDeleteView(generic.DeleteView):
    pass


class VideoDeleteView(generic.DeleteView):
    pass
