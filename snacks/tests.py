from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack


class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='toto', email='toto.test@email.com', password='toto2021pass'
        )

        self.snack = Snack.objects.create(
            title='chips', purchaser=self.user, description='toto likes chips <3'
        )

    def test_string(self):
        self.assertEqual(str(self.snack), 'chips')

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", 'chips')
        self.assertEqual(f"{self.snack.purchaser}", 'toto')
        self.assertEqual(f"{self.snack.description}", 'toto likes chips <3')

    def test_snack_list(self):
        response = self.client.get(reverse('snack_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chips')
        self.assertTemplateUsed(response, 'snack_list.html')

    def test_snack_detail(self):
        response = self.client.get(reverse('snack_detail', args='1'))
        no_response = self.client.get('/1000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertContains(response, 'toto')

    def test_snack_create(self):
        response = self.client.post(
            reverse('snack_create'),
            {
                'title': 'falafel',
                'purchaser': self.user.id,
                'description': 'sandwish',
            }, follow=True
        )

        self.assertContains(response, 'falafel')
        self.assertContains(response, 'Description: sandwish')
        self.assertRedirects(response, reverse('snack_detail', args='2'))

    def test_snack_delete(self):
        response = self.client.get(reverse('snack_delete', args='1'))
        self.assertEqual(response.status_code, 200)

    def test_snack_update(self):
        response = self.client.post(
            reverse('snack_update', args='1'),
            {
                'title': 'shawerma',
                'purchaser': self.user.id,
                'description': 'delicious'

            }
        )

        self.assertRedirects(response, reverse('snack_detail', args='1'))
