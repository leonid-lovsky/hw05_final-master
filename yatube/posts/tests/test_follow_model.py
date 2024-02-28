from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from ..models import Follow

User = get_user_model()


class TestFollowModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        another_user = User.objects.create_user(username='AnotherUser')
        Follow.objects.create(user=user, author=another_user)

    def setUp(self):
        self.follow = Follow.objects.get(id=1)

    def test_user_remote_field_model(self):
        model = self.follow._meta.get_field('user').remote_field.model
        self.assertEqual(model, User)

    def test_user_remote_field_on_delete(self):
        on_delete = (
            self.follow._meta.get_field('user').remote_field.on_delete
        )
        self.assertEqual(on_delete, models.CASCADE)

    def test_user_remote_field_related_name(self):
        related_name = (
            self.follow._meta.get_field('user').remote_field.related_name
        )
        self.assertEqual(related_name, 'follower')

    def test_user_verbose_name(self):
        verbose_name = self.follow._meta.get_field('user').verbose_name
        self.assertEqual(verbose_name, 'Подписчик')

    def test_author_remote_field_model(self):
        model = self.follow._meta.get_field('author').remote_field.model
        self.assertEqual(model, User)

    def test_author_remote_field_on_delete(self):
        on_delete = (
            self.follow._meta.get_field('author').remote_field.on_delete
        )
        self.assertEqual(on_delete, models.CASCADE)

    def test_author_remote_field_related_name(self):
        related_name = (
            self.follow._meta.get_field('author').remote_field.related_name
        )
        self.assertEqual(related_name, 'following')

    def test_author_verbose_name(self):
        verbose_name = self.follow._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор')
