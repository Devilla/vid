# Generated by Django 2.1.5 on 2019-01-14 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsmodel',
            name='parent_comment_id',
            field=models.IntegerField(default=0),
        ),
    ]
