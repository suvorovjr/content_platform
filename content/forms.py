from django import forms
from .models import Post, Video
from users.forms import StylesMixin


class BaseForm(forms.ModelForm):
    class Meta:
        exclude = ('author', 'created_at')


class PostForm(StylesMixin, BaseForm):
    class Meta(BaseForm.Meta):
        model = Post


class VideoForm(StylesMixin, BaseForm):
    class Meta(BaseForm.Meta):
        model = Post
