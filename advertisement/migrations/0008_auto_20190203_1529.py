# Generated by Django 2.1.5 on 2019-02-03 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0007_auto_20190203_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
