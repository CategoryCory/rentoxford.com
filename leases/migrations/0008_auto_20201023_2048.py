# Generated by Django 3.1.1 on 2020-10-24 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0007_auto_20201020_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lease',
            name='initial_payment',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Security deposit'),
        ),
    ]
