from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase

from ..models import Post, Group

User = get_user_model()


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        Post.objects.create(text='Тестовый текст', author=user)

    def setUp(self):
        self.post = Post.objects.get(id=1)

    def test_text_verbose_name(self):
        verbose_name = self.post._meta.get_field('text').verbose_name
        self.assertEqual(verbose_name, 'Текст поста')

    def test_text_help_text(self):
        help_text = self.post._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Введите текст поста')

    def test_pub_date_verbose_name(self):
        verbose_name = self.post._meta.get_field('pub_date').verbose_name
        self.assertEqual(verbose_name, 'Дата публикации')

    def test_pub_date_auto_now_add(self):
        auto_now_add = self.post._meta.get_field('pub_date').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_author_remote_field_model(self):
        model = self.post._meta.get_field('author').remote_field.model
        self.assertEqual(model, User)

    def test_author_remote_field_on_delete(self):
        on_delete = self.post._meta.get_field('author').remote_field.on_delete
        self.assertEqual(on_delete, models.CASCADE)

    def test_author_remote_field_related_name(self):
        related_name = (
            self.post._meta.get_field('author').remote_field.related_name
        )
        self.assertEqual(related_name, 'posts')

    def test_author_verbose_name(self):
        verbose_name = self.post._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор')

    def test_group_remote_field_model(self):
        model = self.post._meta.get_field('group').remote_field.model
        self.assertEqual(model, Group)

    def test_group_remote_field_on_delete(self):
        on_delete = self.post._meta.get_field('group').remote_field.on_delete
        self.assertEqual(on_delete, models.SET_NULL)

    def test_group_remote_field_related_name(self):
        related_name = (
            self.post._meta.get_field('group').remote_field.related_name
        )
        self.assertEqual(related_name, 'posts')

    def test_group_blank(self):
        blank = self.post._meta.get_field('group').blank
        self.assertEqual(blank, True)

    def test_group_null(self):
        null = self.post._meta.get_field('group').null
        self.assertEqual(null, True)

    def test_group_verbose_name(self):
        verbose_name = self.post._meta.get_field('group').verbose_name
        self.assertEqual(verbose_name, 'Группа')

    def test_group_help_text(self):
        help_text = self.post._meta.get_field('group').help_text
        self.assertEqual(help_text, 'Выберите группу')

    def test_image_verbose_name(self):
        verbose_name = self.post._meta.get_field('image').verbose_name
        self.assertEqual(verbose_name, 'Картинка')

    def test_image_upload_to(self):
        upload_to = self.post._meta.get_field('image').upload_to
        self.assertEqual(upload_to, 'posts/')

    def test_image_blank(self):
        blank = self.post._meta.get_field('image').blank
        self.assertEqual(blank, True)

    def test_model_ordering(self):
        ordering = Post._meta.ordering
        self.assertEqual(ordering, ('-pub_date',))

    def test_model_verbose_name(self):
        verbose_name = Post._meta.verbose_name
        self.assertEqual(verbose_name, 'Пост')

    def test_model_verbose_name_plural(self):
        verbose_name_plural = Post._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Посты')

    def test_object_name(self):
        self.assertEqual(self.post.text[:15], str(self.post))
