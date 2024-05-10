from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PostForm


class PostCreateView(CreateView):
    form_class = PostForm
    success_url = reverse_lazy('users:index')
    template_name = 'content/post_form.html'
