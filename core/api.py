# core/api.py

from rest_framework import viewsets, permissions, filters, exceptions
from rest_framework.permissions import IsAuthenticated
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .serializers import (
    UserSerializer, CourseSerializer, EnrollmentSerializer,
    FeedbackSerializer, StatusUpdateSerializer
)

# Custom Permissions
class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'teacher' role to access an endpoint.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'student' role to access an endpoint.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsEnrolledStudent(permissions.BasePermission):
    """
    Custom permission to only allow students enrolled in a course to perform an action.
    This permission is primarily used to check if a student can create feedback.
    It assumes that the user has already been authenticated.
    """
    def has_permission(self, request, view):
        # Safely check for the 'role' attribute to prevent errors with anonymous users.
        if getattr(request.user, 'role', None) != 'student':
            return False

        # For the 'create' action, check if the student is actively enrolled.
        if view.action == 'create':
            course_id = request.data.get('course')
            if not course_id:
                return False
            return Enrollment.objects.filter(
                student=request.user,
                course_id=course_id,
                is_blocked=False
            ).exists()
        
        # Allow other actions (like list or retrieve) for any student.
        return True

# ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only API endpoint for viewing Users.
    
    Provides `list` and `retrieve` actions.
    Supports searching by `username`, `first_name`, and `last_name`.
    Access is restricted to authenticated users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

class CourseViewSet(viewsets.ModelViewSet):
    """
    A full CRUD API endpoint for managing Courses.
    
    - **List & Retrieve:** All authenticated users can view courses.
    - **Create, Update, Delete:** Only authenticated 'teacher' users can create or modify courses.
    
    When a teacher creates a course, they are automatically assigned as the course teacher.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Dynamically set permissions based on the requested action.
        Write actions are restricted to teachers.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Set the teacher of the course to the currently logged-in user.
        """
        serializer.save(teacher=self.request.user)

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing course Enrollments.
    
    Only 'student' users can interact with this endpoint. When a student
    creates an enrollment, they are automatically assigned as the enrollee.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        """
        Set the student for the enrollment to the currently logged-in user.
        """
        serializer.save(student=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing course Feedback.
    
    - **Create:** Only authenticated 'student' users who are enrolled in the
      specified course can create feedback.
    - **List & Retrieve:** All authenticated users can view feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledStudent]

    def perform_create(self, serializer):
        """
        Set the student for the feedback to the currently logged-in user.
        """
        serializer.save(student=self.request.user)

class StatusUpdateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for users to post and view Status Updates.
    
    All authenticated users can create and view status updates. The user who
    creates the update is automatically assigned.
    """
    queryset = StatusUpdate.objects.order_by('-created_at')
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Set the user for the status update to the currently logged-in user.
        """
        serializer.save(user=self.request.user)