from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response

from courses.models import Course, Lesson, Subscription
from courses.pagination import LMSPagination
from courses.serializers import (CourseSerializer, DocsNoPermissionSerializer, DocsSubscriptionResponseSerializer,
                                 DocsSubscriptionSerializer, LessonSerializer)
from courses.tasks import send_message
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = LMSPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        else:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_queryset(self):
        if not IsModerator().has_permission(self.request, self):
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()

    def perform_update(self, serializer):
        course = serializer.save()
        send_message.delay(course.pk)


@extend_schema(
    request=DocsSubscriptionSerializer,
    responses={
        status.HTTP_200_OK: DocsSubscriptionResponseSerializer,
    },
)
class CourseSubscriptionApiView(views.APIView):
    def post(self, *args, **kwargs):
        course_id = self.kwargs.get("pk")
        course = get_object_or_404(Course, pk=course_id)
        is_subscribe = self.request.data.get("subscribe")
        user = self.request.user

        if is_subscribe:
            subscription = user.subscriptions.create(user=user, course=course)
            subscription.save()
            message = f"You've successfully subscribed for '{course.name}'"
        else:
            Subscription.objects.filter(user=user, course=course).delete()
            message = f"Your subscription for '{course.name}' has been cancelled."
        return Response({"message": message})


@extend_schema(
    responses={
        status.HTTP_201_CREATED: LessonSerializer,
        status.HTTP_403_FORBIDDEN: DocsNoPermissionSerializer,
    },
)
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)
    pagination_class = LMSPagination

    def get_queryset(self):
        if not IsModerator().has_permission(self.request, self):
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner,)

    def perform_update(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        send_message.delay(lesson.course.pk)


@extend_schema(
    responses={
        status.HTTP_201_CREATED: LessonSerializer,
        status.HTTP_403_FORBIDDEN: DocsNoPermissionSerializer,
    },
)
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (~IsModerator | IsOwner,)
