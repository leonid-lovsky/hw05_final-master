import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Post

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestPostCreate(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser')

    def setUp(self):
        self.user = User.objects.get(username='TestUser')

    def tearDown(self):
        self.client.logout()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('posts:post_create')
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            reverse('users:login') + '?next='
            + reverse('posts:post_create')
        )

    def test_post_create_page(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('posts:post_create')
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertTrue('is_edit' in response.context)
        self.assertEqual(response.context['is_edit'], False)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_create_post(self):
        self.client.force_login(self.user)
        self.assertEqual(Post.objects.count(), 0)
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.client.post(
            reverse('posts:post_create'),
            data=form_data
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(id=1).text, 'Тестовый текст')
        self.assertEqual(Post.objects.get(id=1).author, self.user)
        self.assertEqual(Post.objects.get(id=1).image, 'posts/small.gif')
