# Generated by Django 3.0.4 on 2020-04-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_contactformmessage_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactformmessage',
            name='subject',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
