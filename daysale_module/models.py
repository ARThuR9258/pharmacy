from django.conf import settings
from django.db import models
# Create your models here.





class DailySale(models.Model):
    date = models.CharField(verbose_name='تاریخ امروز' , null=True , blank=False)
    day = models.CharField(max_length=200 , verbose_name='روز' , null=True , blank=False)
    cash = models.CharField(max_length=200 , verbose_name='فروش نقد' , null=True , blank=True)
    pose_device = models.CharField(max_length=200 , verbose_name='دستگاه پز' , null=True , blank=True)
    mobile_payment = models.CharField(max_length=200 , verbose_name='کارت به کارت' , null=True , blank=True)
    result = models.CharField(max_length=200 , verbose_name='جمع کل' , null=True , blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_sale', null=True)

    def __str__(self):
        return self.date +  '-' + self.day

    class Meta:
        verbose_name = 'فروش ها'
        verbose_name_plural = 'فروش روزانه داروخانه'