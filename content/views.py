from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PostForm


class PostCreateView(CreateView):
    form_class = PostForm
    success_url = reverse_lazy('users:index')
    template_name = 'content/post_form.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание поста'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            post = form.save()
            post.author = self.request.user
            post.author.save()
        return super().form_valid(form)
