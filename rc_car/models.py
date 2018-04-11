from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import uuid

# Create your models here.

class RC_Car(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    owner = models.ForeignKey(User,
                            related_name="Car_Owner",
                            on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime.now)
    last_used = models.DateTimeField(default=datetime.now)
    viewer_list = models.ManyToManyField(User, related_name="viewer_list", blank=True, null=True)
    user_list = models.ManyToManyField(User, related_name="user_list", blank=True, null=True)
    public_watch = models.BooleanField("Public to Watch", default=False)
    public_drive = models.BooleanField("Public to Drive", default=False)
    current_user = models.ForeignKey(User,
                            related_name="Current_User", blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, editable=False)
    password = models.CharField(max_length=200, default="", null=False)

    def __str__(self):
        return self.name
