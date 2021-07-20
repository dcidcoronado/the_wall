from django.db import models
import re
from datetime import datetime
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        NAME_REGEX = re.compile(r'^[A-ZÀ-ÿ\u00d1][a-zÀ-ÿ\u00f1\u00d1]+$')
        LAST_NAME_REGEX = re.compile(r'^[A-ZÀ-ÿ\u00d1][a-zÀ-ÿ\u00f1\u00d1]+$')
        EMAIL_REGEX = re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$')

        if len(postData['first_name']) == 0:
            errors['first_name'] = "Must enter a first name"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors['first_name'] = "Name must start with a capital letter"
            elif len(postData['first_name']) < 2:
                errors['first_name'] = "The first name must be at least 2 characters long"

        if len(postData['last_name']) == 0:
            errors['last_name'] = "Must enter a last name"
        else:
            if not LAST_NAME_REGEX.match(postData['last_name']):
                errors['last_name'] = "Last name must start with a capital letter"
            elif len(postData['last_name']) < 2:
                errors['last_name'] = "The last name must be at least 2 characters long"
        

        if len(postData['birthday']) == 0:
            errors['birthday'] = "Must enter a birthday"        
        else:
            today = datetime.now()
            birth = datetime.strptime(postData['birthday'],'%Y-%m-%d')
            age = today - birth
            age = age.days/365
            if age < 13:
                errors['birthday'] = "User must be older than 13 years old"

        if len(postData['email']) == 0:
            errors['email'] = "Must enter an email"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Must enter a valid email"
            elif User.objects.filter(email=postData['email']):
                errors['email'] = "Must be a new User"

        if len(['password']) == 0:
            errors['password'] = "Must enter a password"
        else:
            if postData['password'] != postData['cpassword']:
                errors['password'] = "Passwords doesn't match"
            elif len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters long"
            elif User.objects.filter(email=postData['email']):
                errors['email'] = "This email is already registered"

        return errors


    def login_validator(self, postData):
        user = User.objects.filter(email=postData['email'])
        errors = {}
        # print(user)
        if len(user) > 0:
            if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) is False:
                errors['user'] = "Invalid user"
        else:
            errors['user'] = "Invalid user"
        return errors    


class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = UserManager()

    # def __repr__(self):
    #     return f'{first_name} {last_name} {email}'

