from django.core.management.base import BaseCommand
from core.models import User, Course, Enrollment, StatusUpdate
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        StatusUpdate.objects.all().delete()
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Creating new data...")
        fake = Faker()

        teachers = []
        for _ in range(5):
            teachers.append(User.objects.create_user(
                username=fake.user_name(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                role='teacher'
            ))

        students = []
        for _ in range(20):
            students.append(User.objects.create_user(
                username=fake.user_name(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                role='student'
            ))

        courses = []
        for i, t in enumerate(teachers):
            for c in range(3):
                # FIX: Changed 'name' to 'title' to match the Course model.
                courses.append(Course(title=f"Course {i}-{c}", description="Demo", teacher=t))
        Course.objects.bulk_create(courses)

        enrollments = []
        for s in students:
            for _ in range(random.randint(1, 5)):
                c = random.choice(courses)
                enrollments.append(Enrollment(student=s, course=c))
        Enrollment.objects.bulk_create(enrollments, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))