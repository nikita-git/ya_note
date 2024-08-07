"""Тест логики."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestNote(TestCase):
    """Тестовый класс заметки."""

    @classmethod
    def setUpTestData(cls):
        """Инициализация."""
        cls.author = User.objects.create(username='test_admin')
        cls.other_author = User.objects.create(username='test_user')
        cls.note = Note.objects.create(
                title='Заголовок',
                text='Текст',
                author=cls.author,
                slug='1'
            )
        cls.urls = (
            ('notes:detail', cls.note.id),
            ('notes:delete', cls.note.id),
            ('notes:edit', cls.note.id),
            ('notes:add', cls.note)
        )

    def test_create_edit_add_note_anonymous(self):
        """Тест заметки с анонимом."""
        for name, args in self.urls:
            with self.subTest(name=name, args=args):
                if name == 'notes:add':
                    url = reverse(name)
                else:
                    url = reverse(name, args=(args,))
                response = self.client.get(url)
                notes_count = Note.objects.count()
                self.assertEqual(notes_count, 1)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
                response = self.client.post(url)
                notes_count = Note.objects.count()
                self.assertEqual(notes_count, 1)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestEditDeleteNote(TestCase):
    """Тестовый класс для проверки редактирования и удаления заметки."""

    NEW_TEXT = 'Новая заметка'
    NEW_TITLE = 'Новый заголовок'
    NEW_SLUG = 'New_slug'

    @classmethod
    def setUpTestData(cls):
        """Инициализация."""
        cls.author = User.objects.create(username='test_admin')
        cls.other_author = User.objects.create(username='test_user')
        cls.note_author = Note.objects.create(
                            title='Заголовок',
                            text='Текст',
                            author=cls.author,
                            slug='1'
        )
        cls.note_other_author = Note.objects.create(
                            title='Заголовок',
                            text='Текст',
                            author=cls.other_author,
                            slug='2'
        )
        cls.form_data = {
            'text': cls.NEW_TEXT,
            'title': cls.NEW_TITLE,
            'slug': cls.NEW_SLUG
        }
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)

    def test_delete_note_auth_user(self):
        """Удаление заметок пользователем."""
        self.assertEqual(Note.objects.count(), 2)
        response = self.author_client.delete(reverse(
            'notes:delete',
            args=(self.note_author.id,))
        )
        self.assertEqual(Note.objects.count(), 1)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

        response = self.other_author_client.delete(reverse(
            'notes:delete',
            args=(self.note_other_author.id,))
        )
        self.assertEqual(Note.objects.count(), 0)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_edit_note_auth_user(self):
        """Изменение заметки пользователем."""
        url_author = reverse('notes:edit', args=(self.note_author.slug,))
        response = self.author_client.post(url_author, data=self.form_data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.note_author.refresh_from_db()
        self.assertEqual(self.note_author.text, self.NEW_TEXT)
        self.assertEqual(self.note_author.title, self.NEW_TITLE)
        self.assertEqual(self.note_author.slug, self.NEW_SLUG)
