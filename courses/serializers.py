from rest_framework import serializers

from courses.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "amount_of_lessons")


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
