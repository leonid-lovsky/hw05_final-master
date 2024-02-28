from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class TestIndex(TestCase):
    def test_index_page(self):
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('index' in response.context)
        self.assertEqual(response.context['index'], True)
        self.assertTemplateUsed(response, 'posts/index.html')


class TestIndexPageObj(TestCase):
    NUMBER_OF_ITEMS = 14

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        posts = []
        for _ in range(cls.NUMBER_OF_ITEMS):
            posts.append(Post(text='Тестовый текст', author=user))
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')

    def test_first_page(self):
        cache.clear()
        response = self.client.get(reverse('posts:index'))
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
        self.assertTemplateUsed(response, 'posts/index.html')

    def test_second_page(self):
        cache.clear()
        response = self.client.get(reverse('posts:index') + '?page=2')
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
        self.assertTemplateUsed(response, 'posts/index.html')


class IndexCacheTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        Post.objects.create(text='Тестовый текст', author=user)

    def test_index_page_cache(self):
        cache.clear()

        response = self.client.get(reverse('posts:index'))
        self.assertTrue('Тестовый текст' in response.content.decode('utf-8'))

        Post.objects.get(id=1).delete()

        response = self.client.get(reverse('posts:index'))
        self.assertTrue('Тестовый текст' in response.content.decode('utf-8'))

        cache.clear()

        response = self.client.get(reverse('posts:index'))
        self.assertFalse('Тестовый текст' in response.content.decode('utf-8'))
