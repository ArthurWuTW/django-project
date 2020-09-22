from django.db import models

# Create your models here.
class Temperature(models.Model):
    temperature = models.FloatField(null=True,
                                    blank=True,
                                    default=None)
    time = models.DateTimeField()

    def __str__(self):
        return 'temperature'

    class Meta:
        verbose_name_plural = 'temperature'


class Humidity(models.Model):
    humidity = models.FloatField(null=True,
                                    blank=True,
                                    default=None)
    time = models.DateTimeField()

    def __str__(self):
        return 'humidity'

    class Meta:
        verbose_name_plural = 'humidity'

class CpuTemperature(models.Model):
    cpuTemperature = models.FloatField(null=True,
                                    blank=True,
                                    default=None)
    time = models.DateTimeField()

    def __str__(self):
        return 'Cpu Temperature'

    class Meta:
        verbose_name_plural = 'Cpu Temperature'
