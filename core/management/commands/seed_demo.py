from django.core.management.base import BaseCommand
from core.models import User, Course, Enrollment
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Creating new data...")
        fake = Faker()

        teachers = [User.objects.create_user(
            username=f'teacher{i}', password='password', first_name=fake.first_name(),
            last_name=fake.last_name(), email=fake.email(), role='teacher'
        ) for i in range(5)]

        students = [User.objects.create_user(
            username=f'student{i}', password='password', first_name=fake.first_name(),
            last_name=fake.last_name(), email=fake.email(), role='student'
        ) for i in range(20)]

        courses_to_create = []
        for teacher in teachers:
            for i in range(random.randint(2, 5)):
                # FIX: Use 'title' to match the Course model.
                courses_to_create.append(
                    Course(title=fake.bs().title(), description=fake.text(), teacher=teacher)
                )
        Course.objects.bulk_create(courses_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))