# Generated by Django 2.1.5 on 2019-02-03 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_auto_20190203_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='memo',
            field=models.CharField(default='dfaa6f86801c492e', max_length=255),
        ),
    ]
