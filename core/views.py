# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages  # Import the messages framework

from .forms import CustomUserCreationForm, CourseForm, FeedbackForm, StatusUpdateForm
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .decorators import teacher_required, student_required

# Registration
def register(request):
    """
    Handle user registration.
    On successful registration, a success message is displayed.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Add a success message to be displayed on the next page
            messages.success(request, f'Welcome, {user.username}! Your account has been created successfully.')
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Dashboards
@login_required
def dashboard_view(request):
    """
    Redirects user to the appropriate dashboard based on their role.
    """
    if request.user.role == 'teacher':
        return redirect('core:teacher_dashboard')
    else:
        return redirect('core:student_dashboard')

@login_required
@teacher_required
def teacher_dashboard_view(request):
    """
    Display the dashboard for teacher users.
    """
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/teacher_dashboard.html', {'courses': courses})

@login_required
@student_required
def student_dashboard_view(request):
    """
    Display the dashboard for student users.
    """
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'core/student_dashboard.html', {'enrollments': enrollments})

# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'core/course_detail.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(teacher_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/create_course.html'
    success_url = reverse_lazy('core:course_list')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model and add a success message.
        """
        form.instance.teacher = self.request.user
        messages.success(self.request, f'Course "{form.instance.title}" created successfully!')
        return super().form_valid(form)

# Function-based views for actions
@login_required
@student_required
def enroll_in_course_view(request, course_id):
    """
    Handle a student's enrollment in a course.
    """
    course = get_object_or_404(Course, id=course_id)
    # get_or_create returns a tuple (object, created)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    
    if created:
        # Add a success message only if the enrollment was newly created.
        messages.success(request, f'You have successfully enrolled in "{course.title}".')
    else:
        # If they were already enrolled, show an info message.
        messages.info(request, f'You are already enrolled in "{course.title}".')
        
    return redirect('core:course_list')

@login_required
@student_required
def submit_feedback_view(request, course_id):
    """
    Handle feedback submission for a course.
    """
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            # Add a success message.
            messages.success(request, 'Thank you! Your feedback has been submitted.')
            return redirect('core:course_detail', pk=course_id)
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback_form.html', {'form': form, 'course': course})

@login_required
@teacher_required
def block_student_view(request, course_id, student_id):
    """
    Allow a teacher to block a student from a course.
    """
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student_id=student_id)
    enrollment.is_blocked = True
    enrollment.save()
    # Add a success message.
    messages.success(request, f'Student "{enrollment.student.username}" has been blocked from the course.')
    return redirect('core:course_detail', pk=course_id)


@login_required
def user_profile_view(request, username):
    """
    Display a user's profile and handle status updates.
    """
    profile_user = get_object_or_404(User, username=username)
    status_updates = StatusUpdate.objects.filter(user=profile_user).order_by('-created_at')
    
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid() and request.user == profile_user:
            status_update = form.save(commit=False)
            status_update.user = request.user
            status_update.save()
            # Add a success message.
            messages.success(request, 'Your status has been updated!')
            return redirect('core:user_profile', username=username)
    else:
        form = StatusUpdateForm()
        
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'status_updates': status_updates,
        'form': form
    })