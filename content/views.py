from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm, VideoForm


class BaseCreateView(generic.CreateView):
    success_url = reverse_lazy('users:index')

    def form_valid(self, form):
        if form.is_valid():
            publication = form.save()
            publication.author = self.request.user
            publication.author.save()
        return super().form_valid(form)


class VideoCreateView(BaseCreateView):
    form_class = VideoForm
    template_name = 'content/video_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание видео'
        return context_data


class PostCreateView(BaseCreateView):
    form_class = PostForm
    template_name = 'content/post_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание поста'
        return context_data


class PostUpdateView(generic.UpdateView):
    pass


class FeedListView(generic.ListView):
    pass


class PostDetailView(generic.DetailView):
    pass


class PostDeleteView(generic.DeleteView):
    pass
