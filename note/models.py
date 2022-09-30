
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
import uuid



class Note(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True )
    date_posted = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 



