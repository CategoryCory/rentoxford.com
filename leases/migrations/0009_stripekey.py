# Generated by Django 3.1.1 on 2020-10-28 03:05

from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0008_auto_20201023_2048'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_publishable_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100))),
                ('stripe_secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100))),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leases.company')),
            ],
        ),
    ]
