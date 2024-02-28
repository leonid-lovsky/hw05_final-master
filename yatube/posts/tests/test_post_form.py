from django.test import TestCase

from ..forms import PostForm
from ..models import Post


class TestPostForm(TestCase):
    def setUp(self):
        self.form = PostForm()

    def test_form_model(self):
        self.assertEqual(self.form._meta.model, Post)

    def test_form_fields(self):
        self.assertEqual(self.form._meta.fields, ('text', 'group', 'image'))
