# Generated by Django 2.1.4 on 2019-01-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curr_time', models.DateTimeField(auto_now_add=True)),
                ('steem_price', models.FloatField(default=0.269)),
                ('smoke_price', models.FloatField(default=0.05)),
                ('whaleshare_price', models.FloatField(default=0.1)),
            ],
        ),
    ]
