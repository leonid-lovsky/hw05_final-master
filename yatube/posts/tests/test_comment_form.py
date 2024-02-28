from django.test import TestCase

from ..forms import CommentForm
from ..models import Comment


class TestCommentForm(TestCase):
    def setUp(self):
        self.form = CommentForm()

    def test_form_model(self):
        self.assertEqual(self.form._meta.model, Comment)

    def test_form_fields(self):
        self.assertEqual(self.form._meta.fields, ('text',))
