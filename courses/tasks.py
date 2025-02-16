from celery import shared_task
from django.core.mail import send_mail

from courses.models import Course, Subscription


@shared_task
def send_message(course_pk):
    course = Course.objects.get(pk=course_pk)
    subscriptions = Subscription.objects.filter(course=course.pk)
    subscribers = [subscription.user.email for subscription in subscriptions]
    subject = "Course update"
    message = (
        f"We would like to inform you that the course '{course.name}' has been updated.\n"
        f"Go to the website to see the latest information"
    )
    send_mail(subject, message, None, subscribers)
