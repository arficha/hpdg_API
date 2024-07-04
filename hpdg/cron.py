from .models import *
import datetime


def dailyJob():
    tokens = Sessions.objects.all()
    for token in tokens:
        if token.end_time < datetime.datetime.now().timestamp():
            User.objects.delete(id=token.id)
    
  