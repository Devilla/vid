# Generated by Django 2.1.5 on 2019-01-29 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customthreadedcomment',
            name='smoke_id',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='customthreadedcomment',
            name='steem_id',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
        migrations.AddField(
            model_name='customthreadedcomment',
            name='whaleshare_id',
            field=models.CharField(blank=True, default='', max_length=1024),
        ),
    ]
