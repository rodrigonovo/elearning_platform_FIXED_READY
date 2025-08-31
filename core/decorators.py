from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import Course, User

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'student':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def teacher_is_course_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['pk'])
        if not request.user.is_authenticated or request.user != course.teacher:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view