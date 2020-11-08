from django.db import models
from .AuthGroup import AuthGroup

class MessageLog(models.Model):
    group = models.OneToOneField(AuthGroup,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL)
    time = models.DateTimeField()
    title = models.CharField(max_length=25)
    log = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'MessageLog'
