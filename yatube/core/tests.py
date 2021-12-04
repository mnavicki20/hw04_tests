from http import HTTPStatus

from django.test import TestCase


class CustomErrorTestClass(TestCase):
    def test_error_page(self):
        """Проверка кодов ответа и используемого шаблона несуществующей
        страницы."""
        response = self.client.get('/nonexist-page/')
        expected_status_code = HTTPStatus.NOT_FOUND
        expected_template = 'core/404.html'
        self.assertEqual(response.status_code, expected_status_code)
        self.assertTemplateUsed(response, expected_template)
