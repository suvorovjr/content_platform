from django import forms
from .models import Post
from users.forms import StylesMixin


class PostForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'your_field': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
