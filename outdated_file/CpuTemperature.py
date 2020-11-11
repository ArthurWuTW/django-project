from django.db import models

class CpuTemperature(models.Model):
    cpuTemperature = models.FloatField(null=True,
                                    blank=True,
                                    default=None)
    time = models.DateTimeField()

    def __str__(self):
        return 'Cpu Temperature'

    class Meta:
        verbose_name_plural = 'Cpu Temperature'
