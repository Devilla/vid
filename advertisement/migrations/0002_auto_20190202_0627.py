# Generated by Django 2.1.5 on 2019-02-02 06:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='ad',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='ad_banner',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='ad_title',
            field=models.CharField(default='title', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advertisement',
            name='currently_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='targeted_tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='total_plays',
            field=models.IntegerField(default=0),
        ),
    ]