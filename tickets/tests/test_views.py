from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from tickets.enums import Urgency
from tickets.models import Ticket


class TestListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='Han', password='Solo', email='han@solo.sk')
        cls.user2 = get_user_model().objects.create_user(username='Kylo', password='Ren', email='kylo@ren.sk')
        cls.public_ticket = mommy.make(Ticket, created_by=cls.user)
        cls.private_ticket = mommy.make(Ticket, created_by=cls.user2, public=False)

    def test_list_view(self):
        self.client.force_login(self.user)
        url = reverse('tickets:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_only_public(self):
        self.client.force_login(self.user)
        url = reverse('tickets:list')
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        self.assertIn(str(self.public_ticket), content)
        self.assertNotIn(str(self.private_ticket), content)


class TestCreateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='maros', password='hmka', email='maros@hmka.sk')

    def test_create_ticket(self):
        self.client.force_login(self.user)
        url = reverse('tickets:create')
        data = {
            'title': 'Im title',
            'description': 'hellooo',
            'urgency': Urgency.LOW,
            'public': True
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        t = Ticket.objects.last()
        self.assertIsNotNone(t)
        self.assertEqual(t.created_by, self.user)
        self.assertTrue(t.public)


class TestUpdateView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='Elon', password='Musk', email='elon@musk.sk')
        cls.user2 = get_user_model().objects.create_user(username='Kylo', password='Ren', email='kylo@ren.sk')
        cls.private_ticket = mommy.make(Ticket, created_by=cls.user, public=False)

    def test_update_ticket(self):
        self.client.force_login(self.user)
        url = reverse('tickets:update', kwargs={'pk': self.private_ticket.pk})
        data = {
            'title': self.private_ticket.title,
            'public': self.private_ticket.public,
            'urgency': Urgency.LOW,
            'description': 'hello musk',
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        t = Ticket.objects.last()
        self.assertIsNotNone(t)
        self.assertEqual(t.description, data['description'])

    def test_update_private_other_user(self):
        self.client.force_login(self.user2)
        url = reverse('tickets:update', kwargs={'pk': self.private_ticket.pk})
        data = {
            'title': self.private_ticket.title,
            'public': self.private_ticket.public,
            'urgency': Urgency.LOW,
            'description': 'cant change anything man',
        }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 403)
