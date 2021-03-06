from email.policy import default
from django.db import models
from django.contrib.auth.models import User


class Institution(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='institution')
    name = models.CharField(max_length=255, null=False)
    logo = models.ImageField(blank=True, null=True, upload_to="logo/", default='default.png')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name