"""Тесты маршрутов."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тестовый класс."""

    @classmethod
    def setUpTestData(cls):
        """Инициализация данных для проведения тестов."""
        # Создали пользователя.
        cls.author = User.objects.create(username='admin')
        cls.another_author = User.objects.create(username='not_admin')
        # Создали заметку.
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )

    # @skip("-OK-")
    def test_pages_availability_anonymous(self):
        """Проверка доступности страниц анониму."""
        urls = (
            ('notes:home', None, HTTPStatus.OK),
            ('users:login', None, HTTPStatus.OK),
            ('users:logout', None, HTTPStatus.OK),
            ('users:signup', None, HTTPStatus.OK),
            ('notes:add', None, HTTPStatus.FOUND)
        )
        for name, args, status in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    # @skip("-OK-")
    def test_pages_availability_author(self):
        """Проверка доступности заметки автору, пользователю."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.another_author, HTTPStatus.NOT_FOUND)
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:detail', 'notes:edit', 'notes:delete', 'notes:add'):
                with self.subTest(user=user, name=name):
                    if name != 'notes:add':
                        url = reverse(name, args=(self.note.slug,))
                    else:
                        url = reverse(name)
                        status = HTTPStatus.OK

                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
