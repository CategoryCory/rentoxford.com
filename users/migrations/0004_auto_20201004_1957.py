# Generated by Django 3.1.1 on 2020-10-05 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200925_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='lease_begin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='lease_end',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='monthly_rent',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='property',
        ),
    ]