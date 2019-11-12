from django.db import models

class UserManager(models.Manager):
    def validator(self, post_data):
        print('post_data: ', post_data)
        errors = {}

        if len(post_data['first_name']) < 2:
            errors["first_name"] = "your first name is too short"
        if len(post_data['last_name']) < 2:
            errors["last_name"] = "your last name is too short"
        if len(post_data['email']) < 5:
            errors["email"] = "your email is too short"
        if len(post_data['password']) < 8:
            errors["password"] = "your password is too short"
        if (post_data['password'] != post_data['password_confirm']):
            errors['password_confirm'] = 'your password doesn\'t match'
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
