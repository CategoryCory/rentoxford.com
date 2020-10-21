# Generated by Django 3.1.1 on 2020-10-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='type',
            field=models.CharField(choices=[('rent', 'Rent'), ('late_1', 'First Late Fee'), ('late_2', 'Second Late Fee')], default='rent', max_length=25),
        ),
    ]
