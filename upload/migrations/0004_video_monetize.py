# Generated by Django 2.1.4 on 2019-01-07 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20190107_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='monetize',
            field=models.BooleanField(default=False),
        ),
    ]