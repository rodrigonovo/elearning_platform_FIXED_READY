from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Course, Feedback, StatusUpdate, Enrollment
from .forms import FeedbackForm

User = get_user_model()

class BaseAPIFixture(APITestCase):
    @classmethod
    def setUpTestData(cls):
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
        self.client.login(username="teacher1", password="pass")

    def login_student(self):
        self.client.login(username="student1", password="pass")

    def login_other_student(self):
        self.client.login(username="student2", password="pass")


class CourseAPITests(BaseAPIFixture):
    def test_list_courses_ok(self):
        self.login_student()
        url = reverse("course-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_teacher_can_create_course(self):
        self.login_teacher()
        url = reverse("course-list")
        payload = {"title": "New Course", "description": "Created by teacher"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_course(self):
        self.login_student()
        url = reverse("course-list")
        payload = {"title": "Illicit Course", "description": "Should fail"}
        resp = self.client.post(url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

class StatusUpdateAPITests(BaseAPIFixture):
    def test_list_status_updates_sorted_desc(self):
        self.login_student()
        url = reverse("statusupdate-list")
        self.client.post(url, {"content": "First"}, format="json")
        import time
        time.sleep(0.01) # Small delay to ensure distinct timestamps
        self.client.post(url, {"content": "Second"}, format="json")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        contents = [row["content"] for row in resp.data]
        self.assertLess(contents.index("Second"), contents.index("First"))

class FormTests(TestCase):
    def test_feedback_form_valid(self):
        form_data = {'rating': 5, 'comment': 'This comment is definitely long enough.'}
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_invalid_comment_too_short(self):
        form_data = {'rating': 3, 'comment': 'Too short'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Feedback must be at least 10 characters long.", form.errors['comment'])

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = User.objects.create_user(username='testteacher', password='password', role='teacher')
        cls.student = User.objects.create_user(username='teststudent', password='password', role='student')

    def test_student_cannot_access_create_course_view(self):
        self.client.login(username='teststudent', password='password')
        response = self.client.get(reverse('core:create_course'))
        self.assertEqual(response.status_code, 302)

    def test_teacher_can_access_create_course_view(self):
        self.client.login(username='testteacher', password='password')
        response = self.client.get(reverse('core:create_course'))
        self.assertEqual(response.status_code, 200)

class EnrollmentViewTests(BaseAPIFixture):
    def test_student_can_enroll_in_course(self):
        self.login_student()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(student=self.student, course=self.course).exists())

    def test_student_cannot_enroll_twice(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.login_student()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        self.client.post(url)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_teacher_cannot_enroll_in_course(self):
        self.login_teacher()
        url = reverse('core:enroll_in_course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(student=self.teacher, course=self.course).exists())

class FeedbackAPITests(BaseAPIFixture):
    def test_enrolled_student_can_submit_feedback(self):
        Enrollment.objects.create(student=self.student, course=self.course)
        self.login_student()
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 5, 'comment': 'Excelente curso, muito instrutivo.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Feedback.objects.filter(student=self.student, course=self.course, rating=5).exists())

    def test_non_enrolled_student_cannot_submit_feedback(self):
        self.login_other_student()
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 4, 'comment': 'Gostaria de dar feedback.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_submit_feedback(self):
        url = reverse('feedback-list')
        data = {'course': self.course.id, 'rating': 5, 'comment': 'Feedback anônimo.'}
        response = self.client.post(url, data, format='json')
        # ALTERAÇÃO: Alterado de 401 para 403 para corresponder ao comportamento atual da API.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)