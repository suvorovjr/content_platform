from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

    def clean_confirm_code(self):
        confirm_code = self.cleaned_data['confirm_code']
        return confirm_code
