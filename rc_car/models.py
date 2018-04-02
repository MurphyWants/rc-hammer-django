from django.db import models
from django.contrib.auth.models import User
from django import forms

import uuid

# Create your models here.

class RC_Car(models.Model):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    owner = models.ForeignKey(User,
                            related_name="Car_Owner",
                            on_delete=models.CASCADE,)
    date_added = models.DateField()
    last_used = models.DateField()
    viewer_list = models.ManyToManyField(User, related_name="viewer_list", blank=True)
    user_list = models.ManyToManyField(User, related_name="user_list", blank=True)
    public_watch = models.BooleanField("Public to Watch", default='False')
    public_drive = models.BooleanField("Public to Drive", default='False')
    password = forms.CharField(widget=forms.PasswordInput, null=True, required=False)

    def __str__(self):
        return self.name
