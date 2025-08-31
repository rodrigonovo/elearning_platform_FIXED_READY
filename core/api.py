from rest_framework import viewsets, permissions, filters, exceptions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Course, Enrollment, Feedback, StatusUpdate
from .serializers import (
    UserSerializer, CourseSerializer, EnrollmentSerializer,
    FeedbackSerializer, StatusUpdateSerializer
)

# Custom Permissions
class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'

# ViewSets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsTeacher]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    # 1. Apenas a permissão de autenticação é verificada aqui.
    # Isto garante que utilizadores não autenticados recebem um erro 401.
    permission_classes = [permissions.IsAuthenticated]

    # 2. A lógica de autorização é movida para o método create.
    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        # Verifica se o utilizador é um aluno.
        if getattr(user, 'role', None) != 'student':
            raise exceptions.PermissionDenied("Apenas alunos podem submeter feedback.")

        # Verifica se o aluno está matriculado.
        is_enrolled = Enrollment.objects.filter(
            student=user,
            course_id=course_id,
            is_blocked=False
        ).exists()

        if not is_enrolled:
            raise exceptions.PermissionDenied("Tem de estar matriculado no curso para submeter feedback.")

        # Se tudo estiver correto, prossegue com a criação do objeto.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class StatusUpdateViewSet(viewsets.ModelViewSet):
    queryset = StatusUpdate.objects.order_by('-created_at')
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)