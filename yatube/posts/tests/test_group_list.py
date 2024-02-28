from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class TestGroupList(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(title='Тестовая группа', slug='test-group')

    def setUp(self):
        self.group = Group.objects.get(slug='test-group')

    def test_group_list_page(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-group'})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('group' in response.context)
        self.assertEqual(response.context['group'], self.group)
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_error_if_not_found(self):
        response = self.client.get(
            reverse('posts:group_list', kwargs={'slug': 'not-found-group'})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestGroupListViewPageObj(TestCase):
    NUMBER_OF_ITEMS = 14

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='TestUser')
        group = Group.objects.create(
            title='Тестовая группа 1', slug='test-group'
        )
        another_group = Group.objects.create(
            title='Тестовая группа 2', slug='test-another-group'
        )
        posts = []
        for _ in range(cls.NUMBER_OF_ITEMS):
            posts.append(
                Post(text='Тестовый текст', author=user, group=group)
            )
            posts.append(
                Post(text='Тестовый текст', author=user, group=another_group)
            )
            posts.append(
                Post(text='Тестовый текст', author=user)
            )
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.user = User.objects.get(username='TestUser')
        self.group = Group.objects.get(slug='test-group')

    def test_first_page(self):
        response = self.client.get(
            reverse(
                'posts:group_list', kwargs={'slug': 'test-group'}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 10)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.user)
                self.assertEqual(item.group, self.group)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/group_list.html')

    def test_second_page(self):
        response = self.client.get(
            reverse(
                'posts:group_list', kwargs={'slug': 'test-group'}
            ) + '?page=2'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 4)
        prev_item = None
        for item in response.context['page_obj']:
            if prev_item:
                self.assertEqual(item.author, self.user)
                self.assertEqual(item.group, self.group)
                self.assertTrue(prev_item.pub_date >= item.pub_date)
                prev_item = item
            else:
                prev_item = item
        self.assertTemplateUsed(response, 'posts/group_list.html')
