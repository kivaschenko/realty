from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 


class OfferTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='John',
                    email='john@example.com', password='JoKe#r11')


    def test_offer_list_view_status_code(self):
        url = reverse('flats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_offer_view_status_code(self):
        self.client.login(username='John', password='JoKe#r11')
        url = reverse('post_offer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_map_view_status_code(self):
        url = reverse('flats_map')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



