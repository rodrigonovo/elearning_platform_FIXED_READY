# core/api.py

from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .serializers import (
    UserSerializer, CourseSerializer, EnrollmentSerializer,
    FeedbackSerializer, StatusUpdateSerializer
)

# Refactoring Mixin
class UserFieldMixin:
    """
    A mixin that sets a specific field on a model instance to the request.user
    during object creation. The viewset using this mixin must define a
    `user_field_on_create` attribute specifying the name of the field.
    e.g., user_field_on_create = 'student'
    """
    user_field_on_create = None

    def perform_create(self, serializer):
        """
        Overrides the default perform_create to inject the request.user.
        """
        if self.user_field_on_create:
            serializer.save(**{self.user_field_on_create: self.request.user})
        else:
            # Fallback to the default DRF behavior if the field name is not specified.
            super().perform_create(serializer)


# Custom Permissions
class IsTeacher(permissions.BasePermission):
    """
    Allows access only to authenticated users with the 'teacher' role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    """
    Allows access only to authenticated users with the 'student' role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

class IsEnrolledStudent(permissions.BasePermission):
    """
    Custom permission to only allow enrolled students to perform an action.
    This permission assumes IsAuthenticated has already been checked.
    """
    def has_permission(self, request, view):
        # This permission can now safely assume the user is authenticated,
        # as the global exception handler will correctly manage unauthenticated users.
        if request.user.role != 'student':
            return False

        if view.action == 'create':
            course_id = request.data.get('course')
            if not course_id:
                return False
            return Enrollment.objects.filter(
                student=request.user,
                course_id=course_id,
                is_blocked=False
            ).exists()
        
        return True

# ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

class CourseViewSet(UserFieldMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    Teachers can create/edit/delete courses.
    Students can only view courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    user_field_on_create = 'teacher'  # Use mixin for perform_create

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class EnrollmentViewSet(UserFieldMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows enrollments to be viewed or created.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]
    user_field_on_create = 'student'  # Use mixin for perform_create

class FeedbackViewSet(UserFieldMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows feedback to be created by enrolled students.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolledStudent]
    user_field_on_create = 'student'  # Use mixin for perform_create

class StatusUpdateViewSet(UserFieldMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to create and view status updates.
    """
    queryset = StatusUpdate.objects.order_by('-created_at')
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    user_field_on_create = 'user'  # Use mixin for perform_create