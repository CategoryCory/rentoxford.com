# Generated by Django 3.1.1 on 2020-09-24 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20200923_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_1',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_2',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_3',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_4',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_5',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='gallery_image_6',
        ),
        migrations.CreateModel(
            name='ListingGalleryImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Image')),
                ('listing', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='listings.listing')),
            ],
        ),
    ]
