from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson
from users.models import User


class LessonUserTestCase(APITestCase):
    """Test cases for common user."""

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.lesson = Lesson.objects.create(name="Lesson 1", owner=self.user)
        self.user2 = User.objects.create(email="user2@user.ru")
        self.lesson2 = Lesson.objects.create(name="Lesson 2", owner=self.user2)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("courses:create_lesson")
        body = {"name": "Lesson 3"}
        request = self.client.post(url, body)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 3)

    def test_lesson_create_error(self):
        url = reverse("courses:create_lesson")
        body = {"name": "My Lesson", "video_url": "https://my.sky.pro"}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("video_url"), ["Link for third-party resources are not allowed."])

    def test_lesson_retrieve(self):
        url = reverse("courses:lesson_detail", args=(self.lesson.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Lesson 1")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_lesson_retrieve_error(self):
        url = reverse("courses:lesson_detail", args=(self.lesson2.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")

    def test_lesson_list(self):
        url = reverse("courses:lesson_list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "video_url": None,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "course": None,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_lesson_update(self):
        url = reverse("courses:update_lesson", args=(self.lesson.pk,))
        body = {"name": "My Lesson"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "My Lesson")

    def test_lesson_delete(self):
        url = reverse("courses:delete_lesson", args=(self.lesson.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)


class LessonModeratorTestCase(APITestCase):
    """Test cases for moderators."""

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.lesson = Lesson.objects.create(name="Lesson 1", owner=self.user)
        self.lesson2 = Lesson.objects.create(name="Lesson 2", owner=self.user)
        self.moder = User.objects.create(email="moder@moder.ru")
        self.moder.groups.create(name="moderators").save()
        self.client.force_authenticate(user=self.moder)

    def test_lesson_create_error(self):
        url = reverse("courses:create_lesson")
        body = {"name": "Moder Lesson"}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_one_retrieve(self):
        url = reverse("courses:lesson_detail", args=(self.lesson.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Lesson 1")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_lesson_two_retrieve(self):
        url = reverse("courses:lesson_detail", args=(self.lesson2.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Lesson 2")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_lesson_list(self):
        url = reverse("courses:lesson_list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 2,
                "next": "http://testserver/lessons?page=2",
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "video_url": None,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "course": None,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_lesson_update(self):
        url = reverse("courses:update_lesson", args=(self.lesson.pk,))
        body = {"name": "Moder Lesson"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Moder Lesson")

    def test_lesson_update_error(self):
        url = reverse("courses:update_lesson", args=(self.lesson.pk,))
        body = {"video_url": "https://my.sky.pro"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.get("video_url"), ["Link for third-party resources are not allowed."])

    def test_lesson_delete_error(self):
        url = reverse("courses:delete_lesson", args=(self.lesson.pk,))
        request = self.client.delete(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")
        self.assertEqual(Lesson.objects.all().count(), 2)


class CourseSubscriptionTestCase(APITestCase):
    """Test cases for course subscription."""

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_subscription(self):
        url = reverse("courses:course_subscription", args=(self.course.pk,))
        body = {"subscribe": True}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("message"), "You've successfully subscribed for 'Course 1'")

        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertTrue(response.get("is_subscribed"))

    def test_course_unsubscription(self):
        url = reverse("courses:course_subscription", args=(self.course.pk,))
        body = {"subscribe": ""}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("message"), "Your subscription for 'Course 1' has been cancelled.")

        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertFalse(response.get("is_subscribed"))


class CourseUserTestCase(APITestCase):
    """Test cases for common user."""

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        url = reverse("courses:course-list")
        body = {"name": "Course 2"}
        request = self.client.post(url, body)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Course 1")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_course_list(self):
        url = reverse("courses:course-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.course.pk,
                        "name": self.course.name,
                        "description": None,
                        "owner": self.user.pk,
                        "amount_of_lessons": 0,
                        "lessons": [],
                        "is_subscribed": False,
                    }
                ],
            },
        )

    def test_course_update(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        body = {"name": "My Course"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "My Course")

    def test_course_delete(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.delete(url)

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)


class CourseModeratorTestCase(APITestCase):
    """Test cases for moderators."""

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.course = Course.objects.create(name="Course 1", owner=self.user)
        self.course2 = Course.objects.create(name="Course 2", owner=self.user)
        self.moder = User.objects.create(email="moder@moder.ru")
        self.moder.groups.create(name="moderators").save()
        self.client.force_authenticate(user=self.moder)

    def test_course_create_error(self):
        url = reverse("courses:course-list")
        body = {"name": "Moder Course"}
        request = self.client.post(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_one_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Course 1")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_course_two_retrieve(self):
        url = reverse("courses:course-detail", args=(self.course2.pk,))
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Course 2")
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_course_list(self):
        url = reverse("courses:course-list")
        request = self.client.get(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response,
            {
                "count": 2,
                "next": "http://testserver/courses/?page=2",
                "previous": None,
                "results": [
                    {
                        "id": self.course.pk,
                        "name": self.course.name,
                        "description": None,
                        "owner": self.user.pk,
                        "amount_of_lessons": 0,
                        "lessons": [],
                        "is_subscribed": False,
                    }
                ],
            },
        )

    def test_course_update(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        body = {"name": "Moder Course"}
        request = self.client.patch(url, body)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("name"), "Moder Course")

    def test_course_delete_error(self):
        url = reverse("courses:course-detail", args=(self.course.pk,))
        request = self.client.delete(url)
        response = request.json()

        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.get("detail"), "You do not have permission to perform this action.")
        self.assertEqual(Course.objects.all().count(), 2)
