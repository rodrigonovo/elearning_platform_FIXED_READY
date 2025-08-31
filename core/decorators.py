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
    
def teacher_is_course_owner_by_id(view_func):
    """Decorator to check if the current user is the teacher of a course, using course_id."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['course_id'])
        if not request.user.is_authenticated or request.user != course.teacher:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_is_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile_user = get_object_or_404(User, username=kwargs.get('username'))
        if not request.user.is_authenticated or request.user != profile_user:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view