# Generated by Django 3.1.1 on 2020-10-01 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance_requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='description',
            field=models.TextField(verbose_name="Please provide a description of the maintenance problem you're having."),
        ),
    ]
