from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import CustomUserCreationForm, CourseForm, FeedbackForm, StatusUpdateForm, ProfileUpdateForm
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .decorators import teacher_required, student_required, user_is_owner, teacher_is_course_owner


def home_view(request):
    """
    Redirects the user from the root URL to a relevant page.
    - Authenticated users are sent to their dashboard.
    - Anonymous users are sent to the login page.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    else:
        return redirect('login')


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
            messages.success(request, f'Welcome, {user.username}! Your account has been created successfully.')
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


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
    
    This view now also includes a form for posting status updates directly
    from the dashboard.
    """
    # Get the student's enrollments to display.
    enrollments = Enrollment.objects.filter(student=request.user)
    
    # Get the student's past status updates.
    status_updates = StatusUpdate.objects.filter(user=request.user).order_by('-created_at')

    # Create an instance of the status update form.
    form = StatusUpdateForm()
    
    # Define the context to pass to the template.
    context = {
        'enrollments': enrollments,
        'status_updates': status_updates,
        'form': form
    }
    
    return render(request, 'core/student_dashboard.html', context)


class CourseListView(ListView):
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'core/course_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['course']
        user = self.request.user
        
        if user.is_authenticated:
            is_enrolled = course.enrollment_set.filter(student=user).exists()
            context['is_enrolled'] = is_enrolled
            
            if user.role == 'student' and is_enrolled:
                has_submitted_feedback = Feedback.objects.filter(student=user, course=course).exists()
                context['has_submitted_feedback'] = has_submitted_feedback
        
        return context


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


@method_decorator(login_required, name='dispatch')
@method_decorator(user_is_owner, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'core/profile_update_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs.get('username'))
    
    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated!')
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the user's profile page after a successful update.
        """
        return reverse('core:user_profile', kwargs={'username': self.object.username})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_is_owner, name='dispatch')
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/course_update_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'Course "{form.instance.title}" updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the course detail page after a successful update.
        """
        return reverse('core:course_detail', kwargs={'pk': self.object.pk})


@login_required
@student_required
def enroll_in_course_view(request, course_id):
    """
    Handle a student's enrollment in a course.
    """
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    
    if created:
        messages.success(request, f'You have successfully enrolled in "{course.title}".')
    else:
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
            messages.success(request, 'Your status has been updated!')
            return redirect('core:user_profile', username=username)
    else:
        form = StatusUpdateForm()
        
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'status_updates': status_updates,
        'form': form
    })