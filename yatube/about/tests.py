from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class Tests(TestCase):
    def test_about_author_reverse(self):
        path = reverse('about:author')
        self.assertEqual(path, '/about/author/')

    def test_about_author_template(self):
        response = self.client.get(reverse('about:author'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/author.html')

    def test_about_tech_reverse(self):
        path = reverse('about:tech')
        self.assertEqual(path, '/about/tech/')

    def test_about_tech_template(self):
        response = self.client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'about/tech.html')
