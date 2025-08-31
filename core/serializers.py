from rest_framework import serializers
from .models import User, Course, Enrollment, Feedback, StatusUpdate

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'real_name', 'photo', 'role']

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserPublicSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'created_at', 'course_material']

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserPublicSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Enrollment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    student = UserPublicSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = '__all__'

class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    class Meta:
        model = StatusUpdate
        fields = '__all__'