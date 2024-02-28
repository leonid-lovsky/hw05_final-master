from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import CommentForm
from ..models import Post, Comment

User = get_user_model()


class TestPostDetail(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        Post.objects.create(text='Тестовый текст', author=user)

    def setUp(self):
        self.post = Post.objects.get(id=1)

    def test_post_detail_page(self):
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('post' in response.context)
        self.assertEqual(response.context['post'], self.post)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], CommentForm)
        self.assertTrue('comments' in response.context)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_error_if_not_found(self):
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestPostDetailComments(TestCase):
    NUMBER_OF_ITEMS = 14

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        post = Post.objects.create(text='Тестовый текст', author=user)
        comments = []
        for _ in range(cls.NUMBER_OF_ITEMS):
            comments.append(
                Comment(post=post, author=user, text='Тестовый комментарий')
            )
        Comment.objects.bulk_create(comments)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.post = Post.objects.get(id=1)

    def test_comments(self):
        response = self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['comments']), 14)
        prev_item = None
        for item in response.context['comments']:
            if prev_item:
                self.assertEqual(item.post, self.post)
                self.assertEqual(item.author, self.user)
                self.assertTrue(prev_item.created >= item.created)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/post_detail.html')
