from django.test import TestCase

from tickets.utils import mul


class TestUtils(TestCase):

    def test_add(self):
        self.assertEqual(mul(3, 5), 15)
