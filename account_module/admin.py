from django.contrib import admin

from account_module.models import User, PasswordResetCode

# Register your models here.

admin.site.register(User)

admin.site.register(PasswordResetCode)