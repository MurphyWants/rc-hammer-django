from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

# Create your models here.

"""

The rc_car class is from AbstractBaseUser so that the car can have their own password
- Variables:
    - Name: Named when created, can be changed
    - Id: a unique uuid created, availible to anyone that has access
    - Owner: assigned when created to the user that created it
    - Date_Added: assigned when created to that date and time
    - Last_used: the last date/time the car itself logged in and pinged the server, default when its created
    - Viewer_List: A list of users that can watch what is happening, empty by default
    - User_List: A list of users that can both watch and control the car, empty by default
    - Public_Watch: A checkbox off by default to let anyone watch what is happening
    - Public_Drive: A checkbox off by default to let anyone drive
    - Current_User: If a user is controlling it they are stored here, otherwise empty
    - Password: Set by the owner, changed by the owner, used for authenticating the car
- Functions:
    - Can_control(User)
        - Given a user, returned True if they are allowed to control it, False otherwise
    - Can_view(User)
        - Given a user, returned True if they are allowed to watch it, False otherwise
    - Is_Online(None)
        - Returns true if last_used is within 2 minutes, False otherwise
    - Password_Correct(Password)
        - Custom authentication, given a password check if that password is the same as the hashed password
        - Used during websockets for authentication

"""

class RC_Car(AbstractBaseUser):
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
    password_lockout = models.BooleanField(default=False, editable=False)
    password_attempts = models.IntegerField(default=0, editable=False)

    last_consumer_ping = models.DateTimeField(default=datetime.now)

    USERNAME_FIELD = 'id'

    def __str__(self):
        return self.name

    def Can_Control(self, input_user):
        if (input_user == self.owner) or (input_user in self.user_list.all()):
            return True
        else:
            return False

    def Can_Watch(self,input_user):
        if (self.Can_Control(input_user)) or (input_user in self.viewer_list.all()):
            return True
        else:
            return False

    def Is_Online(self):
        return self.last_used > datetime.now(timezone.utc) - timedelta(seconds=120)

    def Check_Password(self, input_password):
        if(self.password_lockout == True):
            return False
        elif (self.check_password(input_password)):
            self.password_attempts = 0
            return True
        else:
            self.password_attempts = self.password_attempts + 1
            if (self.password_attempts > 2):
                self.password_lockout = True
            return False
