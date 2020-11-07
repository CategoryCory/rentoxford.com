# Generated by Django 3.1.1 on 2020-11-03 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_payment_stripe_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='confirmation',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]