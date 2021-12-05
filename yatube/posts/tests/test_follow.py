from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Post, User


class FollowTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_author_janka = User.objects.create(
            username='test_janka',
            email='janka_kupala@gmail.com',
            password='Ludzmi_zvacca_1918',
        )
        cls.test_user_kastus = User.objects.create(
            username='test_kastus',
            email='kastus_1863@gmail.com',
            password='Kaho_lubis_1863',
        )
        cls.post = Post.objects.create(
            author=cls.test_author_janka,
            text='Тестовый текст публикации',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.test_user_kastus)

    def test_authorized_client_can_follow_authors(self):
        """Авторизованный пользователь может подписаться на авторов."""
        follow_url = reverse('posts:profile_follow',
                             args=[self.test_author_janka.username])
        self.authorized_client.get(follow_url)
        follow_exists = Follow.objects.filter(
            user=self.test_user_kastus,
            author=self.test_author_janka,
        ).exists()
        # print(f'Кол-во созданных подписок - {Follow.objects.count()}')
        self.assertTrue(follow_exists)

    def test_authorized_client_can_unfollow_authors(self):
        """Авторизованный пользователь может отписаться от авторов."""
        Follow.objects.create(
            user=self.test_user_kastus,
            author=self.test_author_janka,
        )
        unfollow_url = reverse('posts:profile_unfollow',
                               args=[self.test_author_janka.username])
        self.authorized_client.get(unfollow_url)
        follow_exists = Follow.objects.filter(
            user=self.test_user_kastus,
            author=self.test_author_janka,
        ).exists()
        self.assertFalse(follow_exists)

    def test_new_post_appears_for_followers(self):
        """Новая запись пользователя отображается в ленте тех,
        кто на него подписан."""
        Follow.objects.create(
            user=self.test_user_kastus,
            author=self.test_author_janka,
        )
        follow_index_url = reverse('posts:follow_index')
        user_response = self.authorized_client.get(follow_index_url)
        user_content = user_response.context['page_obj']
        self.assertIn(self.post, user_content)

    def test_new_post_does_not_appear_for_nonfollowers(self):
        """Новая запись пользователя не отображается в ленте тех,
        кто на него не подписан."""
        follow_index_url = reverse('posts:follow_index')
        user_response = self.authorized_client.get(follow_index_url)
        user_content = user_response.context['page_obj']
        self.assertNotIn(self.post, user_content)
