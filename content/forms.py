from django import forms
from .models import Post, Video
from common.mixins import StylesMixin


class BaseForm(forms.ModelForm):
    class Meta:
        exclude = ('author', 'created_at')

    def clean_title(self):
        title = str(self.cleaned_data['title'])
        if len(title) < 10:
            raise forms.ValidationError('Заголовок не может быть меньше 10 символов')
        return title

    def clean_body(self):
        body = str(self.cleaned_data['body'])
        if len(body) < 20:
            raise forms.ValidationError('Описание не может быть меньше 20 символов')
        return body


class PostForm(StylesMixin, BaseForm):
    class Meta(BaseForm.Meta):
        model = Post


class VideoForm(StylesMixin, BaseForm):
    class Meta(BaseForm.Meta):
        model = Video
