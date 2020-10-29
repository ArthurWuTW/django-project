from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    activation = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.email)

    class Meta:
        verbose_name_plural = 'Profile'
