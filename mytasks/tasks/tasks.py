from datetime import date

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Task


@shared_task
def send_reminder():
    
    today_date = date.today()
    tasks = Task.objects.filter(due_date__lte=today_date, reminder_sent=False)
    
    reminder_sent_ids = []
    for task in tasks:
        user = task.user
        send_mail(
            'Task Reminder',
            f'Remember to complete your task: {task.title}',
            'from@indusaction.com',
            [user.email],
            fail_silently=False,
        )
        reminder_sent_ids.append(task.id)
    Task.objects.filter(id__in=reminder_sent_ids).update(reminder_sent=True)