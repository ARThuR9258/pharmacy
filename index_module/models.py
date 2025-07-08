from django.db import models
from django.conf import settings

class Drugs(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام دارو')
    category = models.CharField(max_length=200, verbose_name='دسته بندی دارو', null=True, blank=True)
    expiration_date = models.DateField(verbose_name='تاریخ انقضا دارو', null=True, blank=True)
    number = models.CharField(max_length=200 , verbose_name='تعداد دارو')
    description = models.CharField(max_length=400, verbose_name='توضیحات برای این دارو', null=True, blank=True)
    date_in_warehouse = models.CharField(max_length=200,verbose_name='تاریخ ورود دارو به انبار', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='drugs', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'داروها'
        verbose_name_plural = 'داروهای داروخانه'