from django.test import TestCase, RequestFactory
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .handlers import CustomJSONRenderer, custom_exception_handler


class CustomJSONRendererTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.renderer = CustomJSONRenderer()

    def test_render_success(self):
        data = {"key": "value"}
        response = Response(data, status=status.HTTP_200_OK)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":200', rendered_data)
        self.assertIn(b'"message":"Success"', rendered_data)
        self.assertIn(b'"data":{"key":"value"}', rendered_data)

    def test_render_failure(self):
        data = {"detail": "Not found"}
        response = Response(data, status=status.HTTP_404_NOT_FOUND)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":404', rendered_data)
        self.assertIn(b'"message":"Failed"', rendered_data)
        self.assertIn(b'"data":{"detail":"Not found"}', rendered_data)

    def test_render_empty_list(self):
        data = []
        response = Response(data, status=status.HTTP_200_OK)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":200', rendered_data)
        self.assertIn(b'"message":"Success"', rendered_data)
        self.assertIn(b'"data":[]', rendered_data)
        self.assertIn(b'"count":0', rendered_data)

    def test_render_non_empty_list(self):
        data = [{"key": "value1"}, {"key": "value2"}]
        response = Response(data, status=status.HTTP_200_OK)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":200', rendered_data)
        self.assertIn(b'"message":"Success"', rendered_data)
        self.assertIn(b'"data":[{"key":"value1"},{"key":"value2"}]', rendered_data)
        self.assertIn(b'"count":2', rendered_data)

    def test_render_nested_data(self):
        data = {"key": {"subkey": "subvalue"}}
        response = Response(data, status=status.HTTP_200_OK)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":200', rendered_data)
        self.assertIn(b'"message":"Success"', rendered_data)
        self.assertIn(b'"data":{"key":{"subkey":"subvalue"}}', rendered_data)

    def test_render_different_status_code(self):
        data = {"detail": "Unauthorized"}
        response = Response(data, status=status.HTTP_401_UNAUTHORIZED)
        request = self.factory.get('/')
        renderer_context = {'response': response, 'request': request}

        rendered_data = self.renderer.render(data, renderer_context=renderer_context)
        self.assertIn(b'"code":401', rendered_data)
        self.assertIn(b'"message":"Failed"', rendered_data)
        self.assertIn(b'"data":{"detail":"Unauthorized"}', rendered_data)


class CustomExceptionHandlerTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_validation_error(self):
        request = self.factory.get('/')
        exc = exceptions.ValidationError({"field": ["This field is required."]})
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"field": ["This field is required."]}})

    def test_api_exception(self):
        request = self.factory.get('/')
        exc = exceptions.APIException("An error occurred.")
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"message": "An error occurred."})

    def test_generic_exception(self):
        request = self.factory.get('/')
        exc = Exception("A generic error occurred.")
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"message": "A generic error occurred."})

    def test_generic_exception_empty_traceback(self):
        request = self.factory.get('/')
        exc = Exception("A generic error occurred.")
        context = {'request': request}

        with self.assertLogs('apps.api.handlers', level='ERROR') as cm:
            response = custom_exception_handler(exc, context)
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data, {"message": "A generic error occurred."})
            self.assertIn("Exception: Exception - A generic error occurred.", cm.output[0])

    def test_client_error_exception(self):
        request = self.factory.get('/')
        exc = exceptions.NotFound("Not found.")
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"message": "Not found."})

    def test_permission_denied_exception(self):
        request = self.factory.get('/')
        exc = exceptions.PermissionDenied("Permission denied.")
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"message": "Permission denied."})

    def test_not_authenticated_exception(self):
        request = self.factory.get('/')
        exc = exceptions.NotAuthenticated("Authentication credentials were not provided.")
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "Authentication credentials were not provided."})
    
    def test_throttled_exception(self):
        request = self.factory.get('/')
        exc = exceptions.Throttled(wait=60)
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_4xx_status_code_exception(self):
        class CustomClientError(Exception):
            status_code = 418  # Example 4xx status code
            detail = "I'm a teapot"

        request = self.factory.get('/')
        exc = CustomClientError()
        context = {'request': request}

        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.data, {"message": "I'm a teapot"})
