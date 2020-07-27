from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Blog(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(max_length =200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = 
    models.CASCADE)
    time = models.DateTimeField(default=timezone.now)