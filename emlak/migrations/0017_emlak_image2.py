# Generated by Django 3.0.4 on 2020-05-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emlak', '0016_auto_20200513_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='emlak',
            name='image2',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
