from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Follow

User = get_user_model()


class TestProfileFollow(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser')
        User.objects.create_user(username='AnotherUser')

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.another_user = User.objects.get(username='AnotherUser')

    def tearDown(self):
        self.client.logout()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                'posts:profile_follow', kwargs={'username': 'AnotherUser'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next='
            + reverse(
                'posts:profile_follow', kwargs={'username': 'AnotherUser'}
            )
        )

    def test_error_if_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'posts:profile_follow', kwargs={'username': 'NotFoundUser'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_profile_follow_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse(
                'posts:profile_follow', kwargs={'username': 'AnotherUser'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse(
                'posts:profile', kwargs={'username': 'AnotherUser'}
            )
        )

    def test_follow_profile(self):
        self.client.force_login(self.user)
        self.assertTrue(
            not Follow.objects.filter(
                user=self.user, author=self.another_user
            ).exists()
        )
        self.client.get(
            reverse(
                'posts:profile_follow', kwargs={'username': 'AnotherUser'}
            )
        )
        self.assertTrue(
            Follow.objects.filter(
                user=self.user, author=self.another_user
            ).exists()
        )

    def test_self_follow(self):
        self.client.force_login(self.user)
        self.client.get(
            reverse(
                'posts:profile_follow', kwargs={'username': 'TestUser'}
            )
        )
        self.assertFalse(
            Follow.objects.filter(
                user=self.user, author=self.user
            ).exists()
        )
