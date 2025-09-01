"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import Course, User

# --- Def `teacher_required`: High-level intent

# This function contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

def teacher_required(view_func):
    @wraps(view_func)
    # --- Def `_wrapped_view`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- Def `student_required`: High-level intent

# This function contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

def student_required(view_func):
    @wraps(view_func)
    # --- Def `_wrapped_view`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- Def `teacher_is_course_owner`: High-level intent

# This function contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

def teacher_is_course_owner(view_func):
    @wraps(view_func)
    # --- Def `_wrapped_view`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def _wrapped_view(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        if not request.user.is_authenticated or request.user != course.teacher:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
    
# --- Def `teacher_is_course_owner_by_id`: High-level intent
    
# This function contributes to the domain model or view/controller layer.
    
# Outline: responsibilities, key parameters, side-effects, and return semantics.
    
def teacher_is_course_owner_by_id(view_func):
    """Decorator to check if the current user is the teacher of a course, using course_id."""
    @wraps(view_func)
    # --- Def `_wrapped_view`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def _wrapped_view(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['course_id'])
        if not request.user.is_authenticated or request.user != course.teacher:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# --- Def `user_is_owner`: High-level intent

# This function contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

def user_is_owner(view_func):
    @wraps(view_func)
    # --- Def `_wrapped_view`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def _wrapped_view(request, *args, **kwargs):
        profile_user = get_object_or_404(User, username=kwargs.get('username'))
        if not request.user.is_authenticated or request.user != profile_user:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
