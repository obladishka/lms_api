from rest_framework import serializers

from courses.models import Course, Lesson
from courses.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[URLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)

    def get_amount_of_lessons(self, course):
        """Calculating amount of lessons of a course."""
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "owner", "amount_of_lessons", "lessons")
