from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Tests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com', 'secret')
        self.client.login(username='test', password='secret')

    def test_admin(self):
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
