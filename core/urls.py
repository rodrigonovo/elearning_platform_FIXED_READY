from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard and registration views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('register/', views.register, name='register'),
    
    # Action-based function views
    path('courses/<int:course_id>/enroll/', views.enroll_in_course_view, name='enroll_in_course'),
    path('courses/<int:course_id>/feedback/', views.submit_feedback_view, name='submit_feedback'),
    path('courses/<int:course_id>/block/<int:student_id>/', views.block_student_view, name='block_student'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    
    # Class-Based Views for course display and creation
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='create_course'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
]