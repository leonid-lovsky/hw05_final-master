from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post, Follow

User = get_user_model()


class TestProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser')

    def setUp(self):
        self.user = User.objects.get(username='TestUser')

    def test_profile_page(self):
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': 'TestUser'})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('author' in response.context)
        self.assertEqual(response.context['author'], self.user)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_error_if_not_found(self):
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': 'NotFoundUser'})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestProfileViewPageObj(TestCase):
    NUMBER_OF_ITEMS = 14

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        another_user = User.objects.create_user(username='AnotherUser')
        posts = []
        for _ in range(cls.NUMBER_OF_ITEMS):
            posts.append(Post(text='Тестовый текст', author=user))
            posts.append(Post(text='Тестовый текст', author=another_user))
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.another_user = User.objects.get(username='AnotherUser')

    def test_first_page(self):
        response = self.client.get(
            reverse(
                'posts:profile', kwargs={'username': 'TestUser'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 10)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.user)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_second_page(self):
        response = self.client.get(
            reverse(
                'posts:profile', kwargs={'username': 'TestUser'}
            ) + '?page=2'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 4)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.user)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/profile.html')


class TestProfileViewFollowing(TestCase):
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

    def test_user_follows_another_user(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': 'AnotherUser'})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('following' in response.context)
        self.assertEqual(response.context['following'], True)
        self.assertTemplateUsed(response, 'posts/profile.html')

    def test_another_user_not_follows_user(self):
        self.client.force_login(self.another_user)
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': 'TestUser'})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('following' in response.context)
        self.assertEqual(response.context['following'], False)
        self.assertTemplateUsed(response, 'posts/profile.html')
