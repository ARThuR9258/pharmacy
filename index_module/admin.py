from django.contrib import admin

from . import models
from .models import Drugs

# Register your models here.


admin.site.register(Drugs)