from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView
from .forms import UserForm, LoginForm, ConfirmCodeForm
from .services import get_confirm_code, send_sms_code
from .models import User


class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Главная'
        return context_data


class UserCreateView(CreateView):
    template_name = 'users/phone_signin.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:confirm_code')

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            self.request.session['phone_number'] = phone_number
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Вход'
        return context_data


class LoginView(BaseLoginView):
    template_name = 'users/password_signin.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Вход'
        return context_data


class ConfirmCodeView(FormView):
    form_class = ConfirmCodeForm
    template_name = 'users/confirm_code.html'
    success_url = reverse_lazy('users:index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user_code = form.cleaned_data['confirm_code']
            confirm_code = request.session.get('confirm_code')
            print(user_code)
            print(confirm_code)
        else:
            return self.form_valid(form)

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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Подтверждение номера'
        return context_data
