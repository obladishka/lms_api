from rest_framework import serializers

from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
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
        fields = ("id", "name", "description", "amount_of_lessons", "lessons")
