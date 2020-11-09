from django.db import models

class Humidity(models.Model):
    humidity = models.FloatField(null=True,
                                    blank=True,
                                    default=None)
    time = models.DateTimeField()

    def __str__(self):
        return 'humidity'

    class Meta:
        verbose_name_plural = 'humidity'
