from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class RC_Car(models.Model):
    name = models.CharField(max_length=200)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User,
                            related_name="Car_Owner",
                            on_delete=models.CASCADE,)
    date_added = models.DateField()
    last_used = models.DateField()
    viewer_list = models.ManyToManyField(User, related_name="viewer_list")
    user_list = models.ManyToManyField(User, related_name="user_list")
    public_watch = models.BooleanField(False)
    public_drive = models.BooleanField(False)

    def __str__(self):
        return self.name
