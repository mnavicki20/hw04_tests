from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',
        )
        cls.guest_client = Client()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.test_user,
            group=cls.group,
            text='Тестовый текст',
        )

    def test_cache_on_index_page_works_correct(self):
        """Кэширование данных на главной странице работает корректно."""
        response = self.guest_client.get(reverse('posts:index'))
        cached_response_content = response.content
        Post.objects.create(
            author=self.test_user,
            group=self.group,
            text='Создаём вторую публикацию',
        )
        response = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(cached_response_content, response.content)
        cache.clear()
        response = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(cached_response_content, response.content)
