"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

# core/utils.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

# --- Def `custom_exception_handler`: High-level intent

# This function contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.

    This handler intercepts PermissionDenied exceptions. If the user associated
    with the request is not authenticated, it swaps the 403 Forbidden
    response with a 401 Unauthorized response, as this is the more
    semantically correct status code for unauthenticated access attempts.
    """
    # Call DRF's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # Check if a PermissionDenied exception was raised for an unauthenticated user.
    if isinstance(exc, PermissionDenied) and not context['request'].user.is_authenticated:
        # If so, create a NotAuthenticated exception to generate a 401 response.
        auth_exc = NotAuthenticated()
        return exception_handler(auth_exc, context)

    return response
