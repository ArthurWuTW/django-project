from django.db import models

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
