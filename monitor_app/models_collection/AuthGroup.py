from django.db import models

class AuthGroup(models.Model):
    group = models.CharField(max_length=25)

    def __str__(self):
        return str(self.group)

    class Meta:
        verbose_name_plural = 'AuthGroup'
