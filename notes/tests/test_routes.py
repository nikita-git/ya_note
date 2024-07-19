from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from notes.models import Note

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.notes = Note.objects.create(title='Заголовок', text='Заметка')

    def test_home_page(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

def test_detail_page(self):
        url = reverse('note:detail', kwargs={'slug': self.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
