from http import HTTPStatus

from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        """Проверка кодов ответа и используемого шаблона несуществующей
        страницы."""
        response = self.client.get('/nonexist-page/')
        excepted_status_code = HTTPStatus.NOT_FOUND
        excepted_template = 'core/404.html'
        self.assertEqual(response.status_code, excepted_status_code)
        self.assertTemplateUsed(response, excepted_template)
