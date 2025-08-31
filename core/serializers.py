from rest_framework import serializers
from .models import User, Course, Enrollment, Feedback, StatusUpdate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'course_material']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'is_blocked']

class FeedbackSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Feedback
        fields = ['id', 'course', 'student', 'rating', 'comment', 'created_at']

class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StatusUpdate
        fields = ['id', 'user', 'content', 'created_at']