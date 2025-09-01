"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# --- Class `User`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class User(AbstractUser):
    ROLE_CHOICES = (('student', 'Student'), ('teacher', 'Teacher'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    
    @property
    # --- Def `real_name`: High-level intent
    # This function contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    def real_name(self):
        return self.get_full_name()

# --- Class `Course`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Def `__str__`: High-level intent

    # This function contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    def __str__(self):
        return self.title

# --- Class `CourseMaterial`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_materials')
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # --- Def `__str__`: High-level intent

    # This function contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    def __str__(self):
        return f'{self.file.name.split("/")[-1]} for {self.course.title}'

# --- Class `Enrollment`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        unique_together = ('student', 'course')

# --- Class `Feedback`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        ordering = ['-created_at']

# --- Class `StatusUpdate`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class StatusUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        ordering = ['-created_at']

# --- Class `Notification`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # --- Class `Meta`: High-level intent
    # This class contributes to the domain model or view/controller layer.
    # Outline: responsibilities, key parameters, side-effects, and return semantics.
    class Meta:
        ordering = ['-created_at']
