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

class TimePrice(models.Model):
    time = models.DateTimeField()
    price = models.FloatField(null=True,
                              blank=True,
                              default=None)
    product = models.CharField(max_length=25)

    def __str__(self):
        return self.product

    class Meta:
        verbose_name_plural = 'TimePrice'

class GrowthRate(models.Model):
    time = models.DateTimeField(null=True)
    plant_id = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(null=True,
                              blank=True,
                              default=None)

    def __str__(self):
        return str(self.time)+"_"+str(self.plant_id)

    class Meta:
        verbose_name_plural = 'GrowthRate'
