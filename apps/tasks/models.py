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
    
    def total_tasks_count(self):
        return self.tasks.count()
    
    def active_tasks_count(self):
        return self.tasks.filter(is_done=False).count()
    
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
        default=1, null=True, blank=True
    )
    deadline = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position','is_done', 'id']

    def __str__(self):
        return self.name
