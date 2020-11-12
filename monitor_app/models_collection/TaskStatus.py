from django.db import models

class TaskStatus(models.Model):
    task_name = models.CharField(max_length=25)
    status = models.CharField(max_length=25)

    def __str__(self):
        return str(self.task_name)

    class Meta:
        verbose_name_plural = 'TaskStatus'
