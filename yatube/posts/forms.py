from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст публикации',
            'group': 'Группа публикации',
        }
        help_texts = {
            'text': 'Введите текст публикации',
            'group': 'Укажите группу публикации',
        }
