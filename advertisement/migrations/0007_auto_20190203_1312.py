# Generated by Django 2.1.5 on 2019-02-03 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_auto_20190203_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='memo',
            field=models.CharField(max_length=255),
        ),
    ]
