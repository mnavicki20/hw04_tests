from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = User.objects.create(
            username='test_username',
            email='testmail@gmail.com',
            password='Qwerty123',
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='test-group',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            group=cls.group,
            text='Тестовый текст публикации для проверки 15 символов',
            author=cls.test_user,
        )

    def test_model_group_has_correct_object_names(self):
        """Проверка корректности работы __str__ у модели Group ."""
        group = PostModelTest.group
        expected_group_name = group.title
        self.assertEqual(expected_group_name, str(group))

    def test_model_post_has_correct_object_names(self):
        """Проверка корректности работы __str__ у модели Post."""
        post = PostModelTest.post
        expected_post_name = post.text[:15]
        self.assertEqual(expected_post_name, str(post))

    def test_verbose_name(self):
        """verbose_name в полях сопадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'author': 'Автор публикации',
            'text': 'Текст публикации',
            'pub_date': 'Дата публикации',
            'group': 'Группа публикации',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях сопадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст публикации',
            'group': 'Укажите группу публикации',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
