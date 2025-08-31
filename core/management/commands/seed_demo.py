from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Course, Enrollment, Feedback, StatusUpdate
from django.db import transaction
from random import randint, choice

User = get_user_model()

class Command(BaseCommand):
    help = "Seed demo data (teachers, students, courses, enrollments, feedback, updates)"

    def handle(self, *args, **opts):
        with transaction.atomic():
            # Clear (optional)
            Enrollment.objects.all().delete()
            Feedback.objects.all().delete()
            StatusUpdate.objects.all().delete()
            Course.objects.all().delete()
            User.objects.filter(username__startswith="demo_").delete()

            # Users
            teachers = [User(username=f"demo_t{i}", role="teacher") for i in range(1, 3)]
            students = [User(username=f"demo_s{i}", role="student") for i in range(1, 11)]
            User.objects.bulk_create(teachers + students)
            for u in teachers + students:
                u.set_password("pass")
            User.objects.bulk_update(teachers + students, ["password"])

            # Fetch reloaded instances
            teachers = list(User.objects.filter(username__startswith="demo_t", role="teacher"))
            students = list(User.objects.filter(username__startswith="demo_s", role="student"))

            # Courses
            courses = []
            for i, t in enumerate(teachers, start=1):
                for c in range(1, 4):
                    courses.append(Course(name=f"Course {i}-{c}", description="Demo", teacher=t))
            Course.objects.bulk_create(courses)
            courses = list(Course.objects.all())

            # Enrollments
            enrolls = []
            for s in students:
                for c in choice([courses[:3], courses[3:6], courses]):  # variety
                    enrolls.append(Enrollment(student=s, course=c))
            Enrollment.objects.bulk_create(enrolls, batch_size=500)

            # Feedback
            fbs = []
            for e in Enrollment.objects.select_related("student", "course")[:50]:
                fbs.append(Feedback(course=e.course, student=e.student,
                                    rating=randint(3,5), comment="Nice course"))
            Feedback.objects.bulk_create(fbs, batch_size=500)

            # Status updates
            ups = []
            for s in students:
                ups.append(StatusUpdate(user=s, content="Excited to learn!"))
            StatusUpdate.objects.bulk_create(ups, batch_size=500)

        self.stdout.write(self.style.SUCCESS("Seeded demo data. Login demo_t1/demo_t2 (pass: pass) or any demo_s*.")) 
