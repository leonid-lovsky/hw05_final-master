from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from ..models import Post, Comment

User = get_user_model()


class TestCommentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        post = Post.objects.create(text='Тестовый текст', author=user)
        Comment.objects.create(
            post=post, author=user, text='Тестовый комментарий'
        )

    def setUp(self):
        self.comment = Comment.objects.get(id=1)

    def test_post_remote_field_model(self):
        model = self.comment._meta.get_field('post').remote_field.model
        self.assertEqual(model, Post)

    def test_post_remote_field_on_delete(self):
        on_delete = self.comment._meta.get_field('post').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_post_remote_field_related_name(self):
        related_name = (
            self.comment._meta.get_field('post').remote_field.related_name
        )
        self.assertEqual(related_name, 'comments')

    def test_post_verbose_name(self):
        verbose_name = self.comment._meta.get_field('post').verbose_name
        self.assertEqual(verbose_name, 'Пост')

    def test_author_remote_field_model(self):
        model = self.comment._meta.get_field('author').remote_field.model
        self.assertEqual(model, User)

    def test_author_remote_field_on_delete(self):
        on_delete = (
            self.comment._meta.get_field('author').remote_field.on_delete
        )
        self.assertEqual(on_delete, models.CASCADE)

    def test_author_remote_field_related_name(self):
        related_name = (
            self.comment._meta.get_field('author').remote_field.related_name
        )
        self.assertEqual(related_name, 'comments')

    def test_author_verbose_name(self):
        verbose_name = self.comment._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор')

    def test_text_verbose_name(self):
        verbose_name = self.comment._meta.get_field('text').verbose_name
        self.assertEqual(verbose_name, 'Текст комментария')

    def test_text_help_text(self):
        help_text = self.comment._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Введите текст комментария')

    def test_created_verbose_name(self):
        verbose_name = self.comment._meta.get_field('created').verbose_name
        self.assertEqual(verbose_name, 'Дата создания')

    def test_created_auto_now_add(self):
        auto_now_add = self.comment._meta.get_field('created').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_model_ordering(self):
        ordering = Comment._meta.ordering
        self.assertEqual(ordering, ('-created',))

    def test_model_verbose_name(self):
        verbose_name = Comment._meta.verbose_name
        self.assertEqual(verbose_name, 'Комментарий')

    def test_model_verbose_name_plural(self):
        verbose_name_plural = Comment._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Комментарии')
