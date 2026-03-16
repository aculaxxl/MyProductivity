from django.db import models
from django.conf import settings

class Project(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='projects'
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'

    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    name = models.CharField(max_length=255)
    priority = models.IntegerField(
        choices=Priority.choices, 
        default=Priority.LOW
    )
    deadline = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position', 'id']

    def __str__(self):
        return self.name
