from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Course, Notification, CourseMaterial

@receiver(post_save, sender=Enrollment)
def notify_teacher_on_enroll(sender, instance, created, **kwargs):
    if created:
        msg = f"{instance.student.username} enrolled on {instance.course.title}"
        Notification.objects.create(user=instance.course.teacher, message=msg)

@receiver(post_save, sender=CourseMaterial)
def notify_students_on_new_material(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        for enr in course.enrollment_set.select_related("student").all():
            Notification.objects.create(user=enr.student, message=f"New material in {course.title}")