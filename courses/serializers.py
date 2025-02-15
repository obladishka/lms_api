from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema_field, extend_schema_serializer
from rest_framework import serializers

from courses.models import Course, Lesson, Subscription
from courses.validators import URLValidator


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Valid example 1",
            value={
                "video_url": "http://youtube.com/your-lesson",
                "name": "string",
                "description": "string",
                "preview": "string",
                "course": 0,
            },
            request_only=True,
        ),
    ]
)
class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[URLValidator()],
        required=False,
        help_text="Enter your lesson video link. NOTE! You can only provide links for videos posted on Youtube.",
    )

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    amount_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_amount_of_lessons(self, course):
        """Calculating amount of lessons of a course."""
        return Lesson.objects.filter(course=course).count()

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_subscribed(self, course):
        """Returns info whether the user is subscribed to the course or not."""
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = ("id", "name", "description", "owner", "amount_of_lessons", "lessons", "is_subscribed")


class DocsNoPermissionSerializer(serializers.Serializer):
    detail = serializers.CharField(default="You do not have permission to perform this action.")


class DocsSubscriptionSerializer(serializers.Serializer):
    subscribe = serializers.BooleanField()


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Subscribe",
            value={
                "message": "You've successfully subscribed for 'Course name'",
            },
            response_only=True,
        ),
        OpenApiExample(
            "Unsubscribe",
            value={
                "message": "Your subscription for 'Course name' has been cancelled.",
            },
            response_only=True,
        ),
    ]
)
class DocsSubscriptionResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
