# Generated by Django 3.0.4 on 2020-05-13 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emlak', '0015_auto_20200513_1937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emlak',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='emlak',
            name='image3',
        ),
    ]