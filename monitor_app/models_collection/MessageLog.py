from django.db import models
from .AuthGroup import AuthGroup
from django.contrib.auth.models import User

class MessageLog(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default="")
    time = models.DateTimeField()
    title = models.CharField(max_length=25)
    log = models.CharField(max_length=100)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'MessageLog'
