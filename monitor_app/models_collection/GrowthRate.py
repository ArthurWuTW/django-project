from django.db import models

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
