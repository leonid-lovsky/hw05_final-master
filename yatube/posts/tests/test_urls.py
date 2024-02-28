from django.test import TestCase

from django.urls import reverse


class TestPostsURLs(TestCase):
    def test_index_reverse(self):
        path = reverse('posts:index')
        self.assertEqual(path, '/')

    def test_group_list_reverse(self):
        path = reverse('posts:group_list', kwargs={'slug': 'test-group'})
        self.assertEqual(path, '/group/test-group/')

    def test_profile_reverse(self):
        path = reverse('posts:profile', kwargs={'username': 'TestUser'})
        self.assertEqual(path, '/profile/TestUser/')

    def test_post_details_reverse(self):
        path = reverse('posts:post_detail', kwargs={'post_id': 1})
        self.assertEqual(path, '/posts/1/')

    def test_post_edit_reverse(self):
        path = reverse('posts:post_edit', kwargs={'post_id': 1})
        self.assertEqual(path, '/posts/1/edit/')

    def test_create_reverse(self):
        path = reverse('posts:post_create')
        self.assertEqual(path, '/create/')

    def test_add_comment_reverse(self):
        path = reverse('posts:add_comment', kwargs={'post_id': 1})
        self.assertEqual(path, '/posts/1/comment/')

    def test_follow_index_reverse(self):
        path = reverse('posts:follow_index')
        self.assertEqual(path, '/follow/')

    def test_profile_follow_reverse(self):
        path = reverse(
            'posts:profile_follow', kwargs={'username': 'TestUser'}
        )
        self.assertEqual(path, '/profile/TestUser/follow/')

    def test_profile_unfollow_reverse(self):
        path = reverse(
            'posts:profile_unfollow', kwargs={'username': 'TestUser'}
        )
        self.assertEqual(path, '/profile/TestUser/unfollow/')
