# Generated by Django 3.1.1 on 2020-09-23 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
