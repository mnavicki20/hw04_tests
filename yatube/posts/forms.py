from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'text': 'Текст публикации',
            'group': 'Группа публикации',
            'image': 'Картинка публикации',
        }
        help_texts = {
            'text': 'Введите текст публикации',
            'group': 'Укажите группу публикации',
            'image': 'Добавьте картинку к публикации',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'author', 'text')
        labels = {
            'post': 'Пост, к которому оставлен комментарий',
            'author': 'Автор комментария',
            'text': 'Текст комментария',
        }
        help_texts = {
            'post': 'Укажите пост, к которому оставлен комментарий',
            'author': 'Укажите автора комментария',
            'text': 'Введите текст комментария',
        }
