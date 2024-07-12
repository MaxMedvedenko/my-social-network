from django.test import TestCase
from .models import *
# Create your tests here.

class UrlTest(TestCase):
    def test_access (self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

# class PostModelTest (TestCase):
#     def test_create_poll (self):
#         post = Post.objects.create(
#             user = "3",
#             content = "3",
#             image = "",
#             likes_count = "1",

#     )
#         self.assertEqual(post.user, "3")
#         self.assertEqual(post.content, "3")
#         self.assertEqual(post.image, "")
#         self.assertEqual(post.likes_count, "1")
#         self.assertTrue(post.is_active)
