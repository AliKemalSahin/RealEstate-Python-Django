# Generated by Django 3.0.4 on 2020-04-12 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emlak', '0008_auto_20200409_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='emlak',
            name='banyo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='emlak',
            name='binaYasi',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='emlak',
            name='garaj',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='emlak',
            name='salon',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='emlak',
            name='yatakOda',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
