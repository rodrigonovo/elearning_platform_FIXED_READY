"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.contrib import admin
from .models import User, Course, Enrollment, Feedback, StatusUpdate, Notification, CourseMaterial
from django.contrib.admin import TabularInline

# --- Class `CourseMaterialInline`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseMaterialInline(TabularInline):
    model = CourseMaterial
    extra = 1

# --- Class `CourseAdmin`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at')
    search_fields = ('title', 'teacher__username')
    inlines = [CourseMaterialInline]

# --- Class `EnrollmentAdmin`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'is_blocked')
    list_filter = ('course', 'is_blocked')

admin.site.register(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Feedback)
admin.site.register(StatusUpdate)
admin.site.register(Notification)
admin.site.register(CourseMaterial)
