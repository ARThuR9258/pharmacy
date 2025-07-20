from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل کاربر')
    is_verified = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

        def __str__(self):
            return self.username

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
