# core/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Course, Feedback, StatusUpdate, Enrollment
from .forms import FeedbackForm

User = get_user_model()

class BaseAPIFixture(APITestCase):
    """
    A base test case class that provides common setup for API tests,
    including creating teacher and student users, and a course.
    """
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        cls.teacher = User.objects.create_user(
            username="teacher1", password="pass", role="teacher", first_name="Prof", last_name="T"
        )
        cls.student = User.objects.create_user(
            username="student1", password="pass", role="student", first_name="Ana", last_name="S"
        )
        cls.other_student = User.objects.create_user(
            username="student2", password="pass", role="student", first_name="Beto", last_name="O"
        )
        cls.course = Course.objects.create(
            title="Intro to Testing",
            description="Testing with DRF",
            teacher=cls.teacher,
        )

    def login_teacher(self):
        """Helper method to log in as the teacher."""
        self.client.login(username="teacher1", password="pass")

    def login_student(self):
        """Helper method to log in as the primary student."""
        self.client.login(username="student1", password="pass")

    def login_other_student(self):
        """Helper method to log in as the secondary student."""
        self.client.login(username="student2", password="pass")


class CourseAPITests(BaseAPIFixture):
    """Tests for the Course API endpoint."""
    def test_list_courses_ok(self):
        """Ensure authenticated users can list courses."""
        self.login_student()
        url = reverse("course-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_teacher_can_create_course(self):
        """Ensure teachers can create new courses."""
        self.login_teacher()
        url = reverse("course-list")
        payload = {"title": "New Course", "description": "Created by teacher"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_course(self):
        """Ensure students are forbidden from creating new courses."""
        self.login_student()
        url = reverse("course-list")
        payload = {"title": "Illicit Course", "description": "Should fail"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

class StatusUpdateAPITests(BaseAPIFixture):
    """Tests for the Status Update API endpoint."""
    def test_list_status_updates_sorted_desc(self):
        """Ensure status updates are listed in reverse chronological order."""
        self.login_student()
        url = reverse("statusupdate-list")
        self.client.post(url, {"content": "First"}, format="json")
        import time
        time.sleep(0.01)  # Small delay to ensure distinct timestamps
        self.client.post(url, {"content": "Second"}, format="json")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        contents = [row["content"] for row in resp.json()]
        self.assertLess(contents.index("Second"), contents.index("First"))

class FormTests(TestCase):
    """Tests for the application's forms."""
    def test_feedback_form_valid(self):
        """Test the FeedbackForm with valid data."""
        form_data = {'rating': 5, 'comment': 'This comment is definitely long enough.'}
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid_comment_too_short(self):
        """Test the FeedbackForm with an invalidly short comment."""
        form_data = {'rating': 3, 'comment': 'Too short'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Feedback must be at least 10 characters long.", form.errors['comment'])

class ViewTests(TestCase):
    """Tests for standard Django views (non-API)."""
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        cls.teacher = User.objects.create_user(username='testteacher', password='password', role='teacher')
        cls.student = User.objects.create_user(username='teststudent', password='password', role='student')

    def test_student_cannot_access_create_course_view(self):
        """Ensure students are redirected from the 'create course' page."""
        self.client.login(username='teststudent', password='password')
        response = self.client.get(reverse('core:create_course'))
        self.assertEqual(response.status_code, 302)

    def test_teacher_can_access_create_course_view(self):
        """Ensure teachers can access the 'create course' page."""
        self.client.login(username='testteacher', password='password')
        response = self.client.get(reverse('core:create_course'))
        self.assertEqual(response.status_code, 200)

class EnrollmentViewTests(BaseAPIFixture):
    """Tests for the enrollment function-based view."""
    def test_student_can_enroll_in_course(self):
        """Ensure a student can enroll in a course."""
        self.login_student()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_student_cannot_enroll_twice(self):
        """Ensure a student cannot enroll in the same course twice."""
        Enrollment.objects.create(student=self.student, course=self.course)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.login_student()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        self.client.post(url)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_teacher_cannot_enroll_in_course(self):
        """Ensure a teacher cannot enroll in a course as a student."""
        self.login_teacher()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(student=self.teacher, course=self.course).exists())

class FeedbackAPITests(BaseAPIFixture):
    """Tests for the Feedback API endpoint."""
    def test_enrolled_student_can_submit_feedback(self):
        """Ensure an enrolled student can submit feedback."""
        Enrollment.objects.create(student=self.student, course=self.course)
        self.login_student()
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 5, 'comment': 'Excellent course, very instructive.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Feedback.objects.filter(student=self.student, course=self.course, rating=5).exists())

    def test_non_enrolled_student_cannot_submit_feedback(self):
        """Ensure a non-enrolled student is forbidden from submitting feedback."""
        self.login_other_student()
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 4, 'comment': 'I would like to give feedback.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_submit_feedback(self):
        """Ensure an unauthenticated user is unauthorized to submit feedback."""
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 5, 'comment': 'Anonymous feedback.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)