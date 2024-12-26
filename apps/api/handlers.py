import logging
import traceback

from rest_framework import exceptions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import set_rollback


logger = logging.getLogger(__name__)


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code

        response = {
            "code": status_code,
            "count": len(data) if isinstance(data, list) else 0,
            "message": 'Failed' if status_code >= 400 else 'Success',
            "data": data,
        }

        return super().render(response, accepted_media_type, renderer_context)


def custom_exception_handler(exc, context):
    if isinstance(exc, exceptions.ValidationError):
        return Response({"message": exc.detail}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, exceptions.APIException):
        return Response({"message": exc.detail}, status=exc.status_code)

    if hasattr(exc, 'status_code') and str(exc.status_code).startswith('4'):
        return Response({"message": exc.detail}, status=exc.status_code)

    tb = traceback.TracebackException.from_exception(exc)
    if tb.stack:
        frame = tb.stack[-1]
        logger.exception(
            f"Exception: {exc.__class__.__name__} - {exc} in {frame.name} at line {frame.lineno} in {frame.filename}"
        )
    else:
        logger.exception(f"Exception: {exc.__class__.__name__} - {exc}")

    set_rollback()

    return Response({"message": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
