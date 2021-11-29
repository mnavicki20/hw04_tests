from django.test import TestCase, Client
from django.urls import reverse

from http import HTTPStatus

from ..models import Post, Group, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    def test_create_post(self):
        """Отправка валидной формы создаёт публикацию."""
        posts_before = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
            'author': self.authorized_client,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_before + 1)
        last_post = Post.objects.last()
        self.assertEqual(last_post.text, form_data['text'])
        self.assertEqual(last_post.group.id, form_data['group'])


class PostEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание',
        )
        cls.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',
        )
        cls.post = Post.objects.create(
            group=cls.group,
            text='Тестовый текст',
            author=cls.test_user,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    def test_create_post(self):
        """Отправка валидной формы редактирует публикацию."""
        posts_count = Post.objects.count()
        edited_text = 'Отредактированный тестовый текст'
        form_data = {
            'group': self.group.id,
            'text': edited_text,
            'author': self.authorized_client,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id, }),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count)
        edited_post = Post.objects.get(id=self.post.id)
        self.assertEqual(edited_post.text, form_data['text'])
        self.assertEqual(edited_post.group.id, form_data['group'])
