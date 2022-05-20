
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status
from django.db import IntegrityError


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    if (isinstance(exc, (ValidationError, TypeError, ValueError,
                         AttributeError, KeyError, NameError,
                         ObjectDoesNotExist, IntegrityError))):
        if response is None:
            response = Response({})
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.data["error"] = str(exc)

    return response
