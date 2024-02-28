from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post

User = get_user_model()


class TestPostEdit(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        User.objects.create_user(username='AnotherUser')
        Post.objects.create(text='Тестовый текст', author=user)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.another_user = User.objects.get(username='AnotherUser')

    def tearDown(self):
        self.client.logout()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next='
            + reverse('posts:post_edit', kwargs={'post_id': 1})
        )

    def test_error_if_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:post_edit', kwargs={'post_id': 2})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_redirect_if_not_author(self):
        self.client.force_login(self.another_user)
        response = self.client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.client.force_login(self.another_user)

    def test_post_edit_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:post_edit', kwargs={'post_id': 1})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue('is_edit' in response.context)
        self.assertEqual(response.context['is_edit'], True)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_edit_post(self):
        self.client.force_login(self.user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(id=1).text, 'Тестовый текст')
        self.assertEqual(Post.objects.get(id=1).author, self.user)
        form_data = {
            'text': 'Измененный пост',
        }
        response = self.client.post(
            reverse('posts:post_edit', kwargs={'post_id': 1}),
            data=form_data,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1}),
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(id=1).text, 'Измененный пост')
        self.assertEqual(Post.objects.get(id=1).author, self.user)
