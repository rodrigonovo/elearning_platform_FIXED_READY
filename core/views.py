from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, CourseForm, FeedbackForm, StatusUpdateForm
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .decorators import teacher_required, student_required

# Registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Dashboards
@login_required
def dashboard_view(request):
    if request.user.role == 'teacher':
        return redirect('core:teacher_dashboard')
    else:
        return redirect('core:student_dashboard')

@login_required
@teacher_required
def teacher_dashboard_view(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'core/teacher_dashboard.html', {'courses': courses})

@login_required
@student_required
def student_dashboard_view(request):
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
        form.instance.teacher = self.request.user
        return super().form_valid(form)

# Function-based views for actions
@login_required
@student_required
def enroll_in_course_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('core:course_list')

@login_required
@student_required
def submit_feedback_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            return redirect('core:course_detail', pk=course_id)
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback_form.html', {'form': form, 'course': course})

@login_required
@teacher_required
def block_student_view(request, course_id, student_id):
    enrollment = get_object_or_404(Enrollment, course_id=course_id, student_id=student_id)
    enrollment.is_blocked = True
    enrollment.save()
    return redirect('core:course_detail', pk=course_id)


@login_required
def user_profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    status_updates = StatusUpdate.objects.filter(user=profile_user).order_by('-created_at')
    
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid() and request.user == profile_user:
            status_update = form.save(commit=False)
            status_update.user = request.user
            status_update.save()
            return redirect('core:user_profile', username=username)
    else:
        form = StatusUpdateForm()
        
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'status_updates': status_updates,
        'form': form
    })