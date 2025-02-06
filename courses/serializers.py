from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[URLValidator()], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, course):
        """Calculating amount of lessons of a course."""
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """Returns info whether the user is subscribed to the course or not."""
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "owner", "amount_of_lessons", "lessons", "is_subscribed")
