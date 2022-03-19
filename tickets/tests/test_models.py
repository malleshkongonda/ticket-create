from django.contrib.auth import get_user_model
from django.test import TestCase

from tickets.enums import Urgency
from tickets.models import Ticket


class TestTicket(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='Elon', password='Musk', email='elon@musk.sk')
        cls.ticket_angry = Ticket.objects.create(
            title='my title', description='please, help me!', created_by=cls.user, urgency=Urgency.HIGH
        )
        cls.ticket_kind = Ticket.objects.create(title='my title', description='can you help me?', created_by=cls.user, urgency=Urgency.LOW)

    def test_angry_description(self):
        d = self.ticket_angry.get_description()
        self.assertEqual(d, 'please, help me!!!')
