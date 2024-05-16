from django.contrib.auth import login
from common.mixins import SlugifyMixin, TitleMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView
from django.contrib.auth.views import LoginView as BaseLoginView
from .forms import UserForm, LoginForm, ConfirmCodeForm, CreateAuthorForm, ProfileUpdateForm
from .services import get_confirm_code, send_sms_code
from content.models import Post, Video
from .models import User, Author


class IndexView(TitleMixin, TemplateView):
    template_name = 'users/index.html'
    title = 'Главная'


class UserCreateView(TitleMixin, CreateView):
    template_name = 'users/phone_signin.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:confirm_code')
    title = 'Вход'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            confirm_code = get_confirm_code()
            send_sms_code(phone_number=phone_number, confirm_code=confirm_code)
            User.objects.get_or_create(phone_number=phone_number)
            self.request.session['phone_number'] = phone_number
            self.request.session['confirm_code'] = confirm_code
            print(confirm_code)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class LoginView(TitleMixin, BaseLoginView):
    template_name = 'users/password_signin.html'
    form_class = LoginForm
    title = 'Вход'


class ConfirmCodeView(TitleMixin, FormView):
    form_class = ConfirmCodeForm
    template_name = 'users/confirm_code.html'
    success_url = reverse_lazy('users:index')
    title = 'Подтверждение номера'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            phone_number = self.request.session['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            login(self.request, user)
            del self.request.session['confirm_code']
            del self.request.session['phone_number']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data()
        if 'resend' in request.GET:
            phone_number = request.session['phone_number']
            print(phone_number)
            confirm_code = get_confirm_code()
            print(confirm_code)
            self.request.session['confirm_code'] = confirm_code
            send_sms_code(phone_number, confirm_code)
        return self.render_to_response(context_data)


class ProfileView(TitleMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    title = 'Профиль'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(TitleMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Редактирование профиля'

    def get_object(self, queryset=None):
        return self.request.user


class AuthorCreateView(TitleMixin, SlugifyMixin, CreateView):
    form_class = CreateAuthorForm
    model = Author
    template_name = 'users/author_form.html'
    success_url = reverse_lazy('users:index')
    title = 'Стать автором'

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            author = form.save()
            author.user = user
            author.slug = self.get_unique_slug(author.blog_name)
            user.is_author = True
            author.save()
            user.save()
        return super().form_valid(form)


class AuthorListView(TitleMixin, ListView):
    model = Author
    template_name = 'users/author_list.html'
    title = 'Блогеры'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'users/author_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        author = self.get_object()
        posts = Post.objects.filter(author=author).values()
        videos = Video.objects.filter(author=author).values()
        combined_data = sorted(list(posts) + list(videos), key=lambda x: x['created_at'], reverse=True)
        context_data['object_list'] = combined_data
        context_data['title'] = f'Профиль {author.blog_name}'
        return context_data
