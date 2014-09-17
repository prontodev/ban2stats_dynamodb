from django.test import SimpleTestCase
from django.http.request import HttpRequest
from ban2stats.views import token_required



@token_required
def function_for_testing(request, x):
    return x


class TestTokenRequired(SimpleTestCase):

    def test_token_success(self):
        request = HttpRequest()
        request.META = {'HTTP_TOKEN': 'Banana'}
        result = function_for_testing(request, 'echome')
        self.assertEqual(result, 'echome')

    def test_token_fail(self):
        request = HttpRequest()
        request.META = {}
        response = function_for_testing(request, 'echome')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, 'Token is required.')

    def test_client_fail(self):
        response = self.client.get('/')
        self.assertEqual(response.content, 'Token is required.')
