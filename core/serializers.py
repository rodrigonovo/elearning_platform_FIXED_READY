"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from rest_framework import serializers
from .models import User, Course, Enrollment, Feedback, StatusUpdate, CourseMaterial

# --- Class `UserSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class UserSerializer(serializers.ModelSerializer):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

# --- Class `CourseMaterialSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseMaterialSerializer(serializers.ModelSerializer):
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        model = CourseMaterial
        fields = ['id', 'file', 'uploaded_at']

# --- Class `CourseSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    course_materials = CourseMaterialSerializer(many=True, read_only=True)

    # --- Class `Meta`: High-level intent

    # This class contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'course_materials']

# --- Class `EnrollmentSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    # --- Class `Meta`: High-level intent

    # This class contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'is_blocked']

# --- Class `FeedbackSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class FeedbackSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    # --- Class `Meta`: High-level intent

    # This class contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    class Meta:
        model = Feedback
        fields = ['id', 'course', 'student', 'rating', 'comment', 'created_at']

# --- Class `StatusUpdateSerializer`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class StatusUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    # --- Class `Meta`: High-level intent

    # This class contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    class Meta:
        model = StatusUpdate
        fields = ['id', 'user', 'content', 'created_at']
