from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    This model stores the task deatail of the user
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    title = models.CharField(
        max_length=200,
    )
    
    due_date = models.DateField()
    
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    
    reminder_sent = models.BooleanField(
        default=False,
    )
    
    class Meta:
        verbose_name = "Tasks"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
