import unittest
from django.test import Client



class HomeTest(unittest.TestCase):
    def test_home_view_status_code(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)


class ContactTest(unittest.TestCase):
    def test_contact_view_status_code(self):
        client = Client()
        response = client.get('/contact/send_mail/')
        self.assertEqual(response.status_code, 200)