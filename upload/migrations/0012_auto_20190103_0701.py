# Generated by Django 2.1.4 on 2019-01-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0011_auto_20190102_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tags',
            field=models.CharField(default='', max_length=100),
        ),
    ]