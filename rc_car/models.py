from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django import forms

import uuid

# Create your models here.

class RC_Car(AbstractBaseUser):
    name = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    owner = models.ForeignKey(User,
                            related_name="Car_Owner",
                            on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=datetime.now)
    last_used = models.DateTimeField(default=datetime.now)
    viewer_list = models.ManyToManyField(User, related_name="viewer_list", blank=True, null=True, widget=forms.CheckboxSelectMultiple)
    user_list = models.ManyToManyField(User, related_name="user_list", blank=True, null=True, widget=forms.CheckboxSelectMultiple)
    public_watch = models.BooleanField("Public to Watch", default=False)
    public_drive = models.BooleanField("Public to Drive", default=False)
    current_user = models.ForeignKey(User,
                            related_name="Current_User", blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, editable=False)
    password = models.CharField(max_length=200, default="", null=False)

    USERNAME_FIELD = 'id'

    def __str__(self):
        return self.name
