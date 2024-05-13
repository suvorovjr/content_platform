from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from users.models import User
from django import forms


class StylesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number',)

    def is_valid(self):
        valid = super().is_valid()
        if 'phone_number' in self.errors:
            unique_error = 'Пользователь с таким Номер телефона уже существует.'
            if unique_error in self.errors['phone_number']:
                del self.errors['phone_number']
                self.cleaned_data['phone_number'] = self.data['phone_number']
                return True
        return valid

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры.')
        if len(phone_number) != 10:
            raise forms.ValidationError('Номер телефона должен содержать ровно 10 цифр.')
        return phone_number


class LoginForm(StylesMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('phone_number', 'password')


class ConfirmCodeForm(StylesMixin, forms.Form):
    confirm_code = forms.CharField(max_length=6, help_text='Введите шестизначный код из смс сообщения')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_confirm_code(self):
        user_code = self.cleaned_data['confirm_code']
        confirm_code = self.request.session['confirm_code']
        if str(user_code) != str(confirm_code):
            raise forms.ValidationError('Неверный код подтверждения')
        return confirm_code


class FlagAutorForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('blog_username', 'blog_description', 'subscription_price')

    def clean_blog_username(self):
        blog_username = str(self.cleaned_data['blog_username'])
        if len(blog_username) < 3:
            raise forms.ValidationError('Название блога не может быть меньше 3 символов')
        return blog_username

    def clean_blog_description(self):
        blog_description = str(self.cleaned_data['blog_description'])
        if len(blog_description) < 20:
            raise forms.ValidationError('Описание блога не может быть меньше 20 символов')
        return blog_description


class ProfileUpdateForm(StylesMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
