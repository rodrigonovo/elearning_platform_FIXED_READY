from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    
    # Dashboard and registration views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('register/', views.register, name='register'),
    
    # Action-based function views
    path('courses/<int:course_id>/enroll/', views.enroll_in_course_view, name='enroll_in_course'),
    path('courses/<int:course_id>/feedback/', views.submit_feedback_view, name='submit_feedback'),
    path('courses/<int:course_id>/block/<int:student_id>/', views.block_student_view, name='block_student'),

    path('courses/<int:course_id>/add-material/', views.add_course_material_view, name='add_course_material'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    
    # Profile views
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(), name='edit_profile'),
    
    # Class-Based Views for course display and creation
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='create_course'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit_course'),

    # New URL for searching users
    path('search-users/', views.search_users_view, name='search_users'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
 
]