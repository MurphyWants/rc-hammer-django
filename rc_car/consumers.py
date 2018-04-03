from channels import Group
from channels.auth import channel_session_user

@channel_session_user
def ws_connect(message):
    return 0

def ws_disconnect(message):
    return 0

def ws_recieve(message):
    return 0
