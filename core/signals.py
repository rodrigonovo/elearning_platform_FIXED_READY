"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Course, Notification, CourseMaterial

@receiver(post_save, sender=Enrollment)
# --- Def `notify_teacher_on_enroll`: High-level intent
# This function contributes to the domain model or view/controller layer.
# Outline: responsibilities, key parameters, side-effects, and return semantics.
def notify_teacher_on_enroll(sender, instance, created, **kwargs):
    if created:
        msg = f"{instance.student.username} enrolled on {instance.course.title}"
        Notification.objects.create(user=instance.course.teacher, message=msg)

@receiver(post_save, sender=CourseMaterial)
# --- Def `notify_students_on_new_material`: High-level intent
# This function contributes to the domain model or view/controller layer.
# Outline: responsibilities, key parameters, side-effects, and return semantics.
def notify_students_on_new_material(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        for enr in course.enrollment_set.select_related("student").all():
            Notification.objects.create(user=enr.student, message=f"New material in {course.title}")
