# Generated by Django 4.0.4 on 2023-04-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0003_apartment_baths_apartment_beds_apartment_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='car',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='dryer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='mate',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pets',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='washer',
            field=models.BooleanField(default=False),
        ),
    ]