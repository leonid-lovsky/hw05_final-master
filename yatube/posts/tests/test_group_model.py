from django.test import TestCase

from ..models import Group


class TestGroupModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(title='Тестовая группа', slug='test-group')

    def setUp(self):
        self.group = Group.objects.get(id=1)

    def test_title_verbose_name(self):
        verbose_name = self.group._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Название группы')

    def test_title_max_length(self):
        max_length = self.group._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_slug_verbose_name(self):
        verbose_name = self.group._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'slug')

    def test_slug_unique(self):
        unique = self.group._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_description_verbose_name(self):
        verbose_name = self.group._meta.get_field('description').verbose_name
        self.assertEqual(verbose_name, 'Описание')

    def test_description_blank(self):
        blank = self.group._meta.get_field('description').blank
        self.assertEqual(blank, True)

    def test_model_verbose_name(self):
        verbose_name = Group._meta.verbose_name
        self.assertEqual(verbose_name, 'Группа')

    def test_model_verbose_name_plural(self):
        verbose_name_plural = Group._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Группы')

    def test_object_name(self):
        self.assertEqual(self.group.title, str(self.group))
