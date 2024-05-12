from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm, VideoForm


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.title is not None:
            context_data['title'] = self.title
        return context_data


class BaseCreateView(TitleMixin, generic.CreateView):
    success_url = reverse_lazy('users:index')

    def form_valid(self, form):
        if form.is_valid():
            publication = form.save()
            publication.author = self.request.user
            publication.author.save()
        return super().form_valid(form)


class PostCreateView(BaseCreateView):
    form_class = PostForm
    template_name = 'content/post_form.html'
    title = 'Создание поста'


class VideoCreateView(BaseCreateView):
    form_class = VideoForm
    template_name = 'content/video_form.html'
    title = 'Создание видео'


class PostUpdateView(generic.UpdateView):
    pass


class FeedListView(generic.ListView):
    pass


class PostDetailView(generic.DetailView):
    pass


class PostDeleteView(generic.DeleteView):
    pass
