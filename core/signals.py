
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Enrollment, Course, Notification

@receiver(post_save, sender=Enrollment)
def notify_teacher_on_enroll(sender, instance, created, **kwargs):
    if created:
        msg = f"{instance.student.username} enrolled on {instance.course.name}"
        Notification.objects.create(user=instance.course.teacher, message=msg)

@receiver(pre_save, sender=Course)
def detect_materials_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = Course.objects.get(pk=instance.pk)
    except Course.DoesNotExist:
        return
    if old.materials != instance.materials and instance.materials:
        # materials file changed/added
        for enr in instance.enrollments.select_related("student").all():
            Notification.objects.create(user=enr.student, message=f"New material in {instance.name}")
