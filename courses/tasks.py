import datetime

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from courses.models import Course, Subscription
from users.models import User


@shared_task
def send_message(course_pk):
    """Sending message to subscribed users after the course is updated."""
    course = Course.objects.get(pk=course_pk)
    subscriptions = Subscription.objects.filter(course=course.pk)
    subscribers = [subscription.user.email for subscription in subscriptions]
    subject = "Course update"
    message = (
        f"We would like to inform you that the course '{course.name}' has been updated.\n"
        f"Go to the website to see the latest information"
    )
    send_mail(subject, message, None, subscribers)


@shared_task
def block_inactive_users():
    """Blocking inactive users (no activity within 1 month)."""
    today = timezone.now().today()
    delta = datetime.timedelta(days=30)
    last_login = today - delta
    non_active_users = User.objects.filter(last_login__lte=last_login)

    if non_active_users:
        for user in non_active_users:
            user.is_active = False
            user.save()
