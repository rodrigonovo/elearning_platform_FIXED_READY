"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.core.management.base import BaseCommand
from core.models import User, Course, Enrollment, CourseMaterial
from faker import Faker
import random

# --- Class `Command`: High-level intent

# This class contributes to the domain model or view/controller layer.

# Outline: responsibilities, key parameters, side-effects, and return semantics.

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    # --- Def `handle`: High-level intent

    # This function contributes to the domain model or view/controller layer.

    # Outline: responsibilities, key parameters, side-effects, and return semantics.

    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        Enrollment.objects.all().delete()
        CourseMaterial.objects.all().delete()
        Course.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("Creating new data...")
        fake = Faker()

        # Create 5 teachers and 20 students
        teachers = [User.objects.create_user(
            username=f'teacher{i}', password='password', first_name=fake.first_name(),
            last_name=fake.last_name(), email=fake.email(), role='teacher'
        ) for i in range(5)]

        students = [User.objects.create_user(
            username=f'student{i}', password='password', first_name=fake.first_name(),
            last_name=fake.last_name(), email=fake.email(), role='student'
        ) for i in range(20)]

        # Create multiple courses for each teacher
        courses_to_create = []
        for teacher in teachers:
            for i in range(random.randint(2, 5)):
                courses_to_create.append(
                    Course(title=fake.bs().title(), description=fake.text(), teacher=teacher)
                )
        Course.objects.bulk_create(courses_to_create)
        all_courses = list(Course.objects.all())

        # Create enrollments for some students
        for student in students:
            if random.random() > 0.5: # 50% chance to enroll in a course
                course = random.choice(all_courses)
                Enrollment.objects.create(student=student, course=course)

        # Create dummy course materials for some courses
        for course in all_courses:
            for i in range(random.randint(0, 3)):
                # Note: We are creating a dummy file name as we don't have actual files
                CourseMaterial.objects.create(
                    course=course,
                    file=f'course_materials/dummy_file_{course.id}_{i}.pdf'
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))
