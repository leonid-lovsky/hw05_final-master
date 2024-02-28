from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Follow, Post

User = get_user_model()


class TestFollowIndex(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        another_user = User.objects.create_user(username='AnotherUser')
        Follow.objects.create(user=user, author=another_user)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.another_user = User.objects.get(username='AnotherUser')

    def tearDown(self):
        self.client.logout()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next='
            + reverse('posts:follow_index')
        )

    def test_follow_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('follow' in response.context)
        self.assertEqual(response.context['follow'], True)
        self.assertTemplateUsed(response, 'posts/follow.html')


class TestFollowIndexPageObj(TestCase):
    NUMBER_OF_ITEMS = 14

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        another_user = User.objects.create_user(username='AnotherUser')
        Follow.objects.create(user=user, author=another_user)
        posts = []
        for _ in range(cls.NUMBER_OF_ITEMS):
            posts.append(Post(text='Тестовый текст', author=user))
            posts.append(Post(text='Тестовый текст', author=another_user))
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.another_user = User.objects.get(username='AnotherUser')

    def test_first_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 10)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.another_user)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/follow.html')

    def test_second_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:follow_index') + '?page=2'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 4)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.another_user)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/follow.html')
