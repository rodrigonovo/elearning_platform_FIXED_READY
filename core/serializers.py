# core/serializers.py

from rest_framework import serializers
from .models import User, Course, Enrollment, Feedback, StatusUpdate

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Provides a serialized representation of a user, including their ID,
    username, name, and role.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    
    Includes a read-only nested representation of the 'teacher' user.
    """
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'course_material']

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.
    
    Includes read-only nested representations of the 'student' and 'course'.
    """
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'is_blocked']

class FeedbackSerializer(serializers.ModelSerializer):
    """
    Serializer for the Feedback model.
    
    The 'student' is read-only and automatically set to the logged-in user upon creation.
    The 'course' is a writeable field, expecting the primary key of the course
    for which feedback is being submitted.
    """
    student = UserSerializer(read_only=True)
    # The 'course' field is writeable by its primary key.
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Feedback
        fields = ['id', 'course', 'student', 'rating', 'comment', 'created_at']

class StatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the StatusUpdate model.
    
    The 'user' is read-only and is automatically set to the logged-in user
    when a new status update is created.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = StatusUpdate
        fields = ['id', 'user', 'content', 'created_at']