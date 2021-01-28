from django.db import models

class Connections(models.Model):
    server_name = models.CharField(max_length=25)
    number = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    def __str__(self):
        return str(server_name)

    class Meta:
        verbose_name_plural = 'connections'
