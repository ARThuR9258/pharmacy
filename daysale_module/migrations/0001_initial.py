# Generated by Django 5.2.3 on 2025-07-24 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DailySale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True, verbose_name='تاریخ امروز')),
                ('day', models.CharField(max_length=200, null=True, verbose_name='روز')),
                ('cash', models.CharField(blank=True, max_length=200, null=True, verbose_name='فروش نقد')),
                ('pose_device', models.CharField(blank=True, max_length=200, null=True, verbose_name='دستگاه پز')),
                ('mobile_payment', models.CharField(blank=True, max_length=200, null=True, verbose_name='کارت به کارت')),
                ('result', models.CharField(max_length=200, null=True, verbose_name='جمع کل')),
            ],
            options={
                'verbose_name': 'فروش ها',
                'verbose_name_plural': 'فروش روزانه داروخانه',
            },
        ),
    ]
