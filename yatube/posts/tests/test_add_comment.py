from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Post

User = get_user_model()


class TestAddComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        Post.objects.create(text='Тестовый текст', author=user)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.post = Post.objects.get(id=1)

    def tearDown(self):
        self.client.logout()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('posts:add_comment', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next='
            + reverse('posts:add_comment', kwargs={'post_id': 1})
        )

    def test_error_if_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:add_comment', kwargs={'post_id': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_comment(self):
        self.client.force_login(self.user)
        self.assertEqual(self.post.comments.count(), 0)
        form_data = {
            'text': 'Тестовый комментарий'
        }
        response = self.client.post(
            reverse('posts:add_comment', kwargs={'post_id': 1}),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(
            self.post.comments.get(id=1).text, 'Тестовый комментарий'
        )
        self.assertEqual(self.post.comments.get(id=1).author, self.user)
