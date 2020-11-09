from django.db import models
from django.contrib.auth.models import User
from .AuthGroup import AuthGroup

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)
    activated = models.BooleanField(default=False)
    permission = models.OneToOneField(AuthGroup,
                                      blank=True,
                                      null=True,
                                      on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user.email)

    class Meta:
        verbose_name_plural = 'Profile'
