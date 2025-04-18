from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):

    name = models.CharField(max_length=150, verbose_name="course title", help_text="Enter your course title")
    preview = models.ImageField(
        upload_to="courses/course_preview",
        verbose_name="course preview",
        help_text="Upload your course preview",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="course description", help_text="Enter your course description", null=True, blank=True
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="owner",
        help_text="Select the owner",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"


class Lesson(models.Model):

    name = models.CharField(max_length=150, verbose_name="lesson title", help_text="Enter your lesson title")
    description = models.TextField(
        verbose_name="lesson description", help_text="Enter your lesson description", null=True, blank=True
    )
    preview = models.ImageField(
        upload_to="courses/lesson_preview",
        verbose_name="lesson preview",
        help_text="Upload your lesson preview",
        null=True,
        blank=True,
    )
    video_url = models.URLField(
        verbose_name="lesson video link", help_text="Enter your lesson video link", null=True, blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="course",
        help_text="Select the course",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="owner",
        help_text="Is automatically filled with the current user's data",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.course})"

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"


class Subscription(models.Model):

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="user",
        help_text="Select the user",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="course",
        help_text="Select the course",
    )
