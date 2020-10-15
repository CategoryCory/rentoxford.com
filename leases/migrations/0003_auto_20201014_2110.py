# Generated by Django 3.1.1 on 2020-10-15 02:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0002_auto_20201012_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('street_address', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('state', models.CharField(blank=True, max_length=25)),
                ('zip_code', models.CharField(blank=True, max_length=25)),
                ('phone_number', models.CharField(blank=True, max_length=25)),
                ('contact_email', models.EmailField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='LeaseDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lease_document', models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name='Lease Document')),
                ('lease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leases.lease')),
            ],
            options={
                'verbose_name': 'Lease Document',
                'verbose_name_plural': 'Lease Documents',
            },
        ),
        migrations.AddField(
            model_name='lease',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leases.company'),
        ),
    ]
