"""
Core views for the eLearning platform.

This file uses a mix of function-based views for simple actions and Class-Based
Views (CBVs) for more complex, model-related operations like listing, creating,
and updating objects, following Django best practices.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView

# Import forms and models
from .forms import CourseForm, FeedbackForm, StatusUpdateForm, CustomUserCreationForm
from .models import Course, Enrollment, Notification, StatusUpdate, User

# ====================================================================
# Function-Based Views (For unique actions and dashboards)
# ====================================================================

@login_required
def dashboard_view(request):
    """Redirects a logged-in user to their role-specific dashboard."""
    if request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

@login_required
def student_dashboard_view(request):
    """Displays the dashboard for a student."""
    if request.user.role != 'student':
        return HttpResponseForbidden("You are not authorized to view this page.")
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    status_update_form = StatusUpdateForm()
    context = {
        'enrollments': enrollments,
        'notifications': notifications,
        'status_update_form': status_update_form,
    }
    return render(request, 'core/student_dashboard.html', context)

@login_required
def teacher_dashboard_view(request):
    """Displays the dashboard for a teacher."""
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not authorized to view this page.")
    courses = Course.objects.filter(teacher=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'courses': courses,
        'notifications': notifications,
    }
    return render(request, 'core/teacher_dashboard.html', context)

def register(request):
    """Handles new user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- FIX: Restoring the missing function-based views for specific actions ---

@login_required
def enroll_in_course_view(request, course_id):
    """Handles the logic for a student to enroll in a course."""
    course = get_object_or_404(Course, id=course_id)
    if request.user.role == 'student':
        Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('course_list')

@login_required
def submit_feedback_view(request, course_id):
    """Handles the logic for a student to submit feedback for a course."""
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            return redirect('course_list')
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback_form.html', {'form': form, 'course': course})

@login_required
def block_student_view(request, course_id, student_id):
    """Handles a teacher's request to block or unblock a student from a course."""
    if request.user.role != 'teacher':
        return HttpResponseForbidden("You are not authorized to perform this action.")
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student_id=student_id, course__teacher=request.user)
    enrollment.is_blocked = not enrollment.is_blocked
    enrollment.save()
    return redirect('teacher_dashboard')

@login_required
def user_profile_view(request, username):
    """Displays a user's public-facing profile page."""
    profile_user = get_object_or_404(User, username=username)
    status_updates = StatusUpdate.objects.filter(user=profile_user).order_by('-created_at')
    context = {
        'profile_user': profile_user,
        'status_updates': status_updates,
    }
    return render(request, 'core/profile.html', context)


# ====================================================================
# Class-Based Views (For displaying lists and details)
# ====================================================================

class CourseListView(LoginRequiredMixin, ListView):
    """Displays a list of all available courses."""
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Allows teachers to create a new course."""
    model = Course
    form_class = CourseForm
    template_name = 'core/create_course.html'
    success_url = '/courses/'

    def test_func(self):
        return self.request.user.role == 'teacher'

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

class CourseDetailView(LoginRequiredMixin, DetailView):
    """Displays the details for a single course."""
    model = Course
    template_name = 'core/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = Enrollment.objects.filter(course=self.object).select_related('student')
        return context