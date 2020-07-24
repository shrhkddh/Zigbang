from django.db import models

class User(models.Model):
    email           = models.EmailField(max_length = 100, null = True, blank = True)
    password        = models.CharField(max_length  = 100, null = True, blank = True)
    name            = models.CharField(max_length  = 50)
    phone_number    = models.OneToOneField('AuthSMS', on_delete = models.SET_NULL, null=True, blank=True)
    social_login_id = models.CharField(max_length = 50, null = True, blank = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'

class AuthSMS(models.Model):
    phone_number = models.CharField(max_length = 20, unique=True)
    auth_number  = models.CharField(max_length = 4)
    updated_at   = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'auth_sms'
