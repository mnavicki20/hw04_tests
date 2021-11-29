from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from yatube.settings import ITEMS_PER_PAGE

from ..models import Post, Group

User = get_user_model()


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',
        )
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user)

    # Проверка используемых шаблонов
    def test_pages_use_correct_templates(self):
        """URL-адрес использует корректный шаблон."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html':
                reverse('posts:group_posts', args=[PostViewsTest.group.slug]),
            'posts/profile.html':
                reverse('posts:profile',
                        args=[PostViewsTest.test_user.username]),
            'posts/post_detail.html':
                reverse('posts:post_detail', args=[PostViewsTest.post.id]),
            'posts/create_post.html':
                reverse('posts:post_edit', args=[PostViewsTest.post.id]),
            'posts/create_post.html': reverse('posts:post_create'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверка отражения поста при указании группы
    # на страницах index, group, profile
    def test_new_post_appears_on_pages(self):
        """Новый пост отображается на страницах index, group, profile"""
        expected_context = self.post
        urls_pages = [
            reverse('posts:index'),
            reverse('posts:group_posts', args=[PostViewsTest.group.slug]),
            reverse('posts:profile', args=[PostViewsTest.test_user.username]),
        ]
        for url in urls_pages:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(len(response.context['page_obj']), 1)
                current_context = response.context['page_obj'][0]
                self.assertEqual(current_context, expected_context)

    # Проверка того, что пост не попал не в свою группу
    def test_new_post_does_not_appear_in_other_group(self):
        """Новый пост не отображается не в свойе группе."""
        other_group = Group.objects.create(
            title='Другой тестовый заголовок',
            slug='other-test-group',
            description='Другое тестовое описание',
        )
        other_group_url = reverse('posts:group_posts', args=[other_group.slug])
        response = self.authorized_client.get(other_group_url)
        self.assertNotIn(self.post, response.context['page_obj'])


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.test_user)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-group',
            description='Тестовое описание',
        )
        for item in range(13):
            cls.post = Post.objects.create(
                author=cls.test_user,
                group=cls.group,
                text=f'Тестовый текст поста номер {item}',
            )

    def test_paginator_for_index_profile_group(self):
        """Паджинатор на страницах index, profile, group работает корректно."""
        first_page_len = ITEMS_PER_PAGE
        second_page_len = Post.objects.count() - ITEMS_PER_PAGE
        context = {
            reverse('posts:index'): first_page_len,
            reverse('posts:index') + '?page=2': second_page_len,
            reverse('posts:group_posts', args=[PaginatorViewsTest.group.slug]):
            first_page_len,
            reverse('posts:group_posts', args=[PaginatorViewsTest.group.slug])
            + '?page=2': second_page_len,
            reverse('posts:profile',
                    args=[PaginatorViewsTest.test_user.username]):
            first_page_len,
            reverse('posts:profile',
                    args=[PaginatorViewsTest.test_user.username]) + '?page=2':
            second_page_len,
        }
        for requested_page, page_len in context.items():
            with self.subTest(requested_page=requested_page):
                response = self.authorized_client.get(requested_page)
                self.assertEqual(len(response.context['page_obj']), page_len)
