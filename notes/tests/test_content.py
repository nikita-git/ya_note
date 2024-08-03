"""Тесты контента."""
from collections import Counter

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from notes.models import Note

User = get_user_model()


class TestPageNotesList(TestCase):
    """Тестовый класс."""

    NOTES_LIST_URL = reverse_lazy('notes:list')
    COUNT_NOTES = 50

    @classmethod
    def setUpTestData(cls):
        """Инициализация данных для проведения тестов."""
        cls.author = User.objects.create(username='test_admin')
        cls.all_notes = [Note(
            title=f'Заголовок {index + 1}',
            text='Текст',
            author=cls.author,
            slug=f'{index}'
        ) for index in range(cls.COUNT_NOTES)]

        Note.objects.bulk_create(cls.all_notes)

    def test_notes_count_author(self):
        """Проверка количества отображаемых записей."""
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, self.COUNT_NOTES)

    def test_unique_address_note(self):
        """Проверка уникальности адреса записи."""
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        slug_list = [
            x for lst in map(list,
                             response.context['object_list']
                             .values_list('slug'))
            for x in lst
        ]
        slug_counter = sum(Counter(slug_list).values())
        self.assertEquals(slug_counter, self.COUNT_NOTES)
