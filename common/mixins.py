from pytils.translit import slugify


class SlugifyMixin:
    model = None

    def get_unique_slug(self, slug_field):
        base_slug = slugify(slug_field)
        slug = base_slug
        count = 1
        while self.model.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{count}'
            count += 1
        return slug


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.title is not None:
            context_data['title'] = self.title
        return context_data


class StylesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
