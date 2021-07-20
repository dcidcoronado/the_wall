from django.db import models
import re
from datetime import datetime
import bcrypt
from login_registration_app.models import User

# Create your models here.
class MessageManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['message']) == 0:
            errors['message'] = 'Please, leave a message'
        
        return errors


class CommentManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if len(postData['comment']) == 0:
            errors['comment'] = 'Please, leave a comment'

        return errors



class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = MessageManager()

class Comment(models.Model):
    message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

