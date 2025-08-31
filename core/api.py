from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .serializers import (UserPublicSerializer, CourseSerializer, EnrollmentSerializer,
                          FeedbackSerializer, StatusUpdateSerializer)


class IsTeacherWriteOrAuthenticatedRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner_field = getattr(obj, 'user', getattr(obj, 'student', None))
        return owner_field == request.user

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request):
        q = request.query_params.get("q", "").strip()
        qs = self.get_queryset()
        if q:
            qs = qs.filter(Q(username__icontains=q) | Q(real_name__icontains=q))
        return Response(UserPublicSerializer(qs[:50], many=True).data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("teacher").all().order_by("-created_at")
    serializer_class = CourseSerializer
    permission_classes = [IsTeacherWriteOrAuthenticatedRead]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Enrollment.objects.select_related("student", "course", "course__teacher").all().order_by("-enrolled_at")
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related("student", "course").order_by("-created_at")
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class StatusUpdateViewSet(viewsets.ModelViewSet):
    # FIX: Set the queryset directly on the class to enforce default ordering.
    queryset = StatusUpdate.objects.select_related("user").order_by("-created_at")
    serializer_class = StatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)