# Generated by Django 2.1.5 on 2019-01-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('channel_name', models.CharField(blank=True, max_length=255)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('is_ad_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('channel_cover', models.CharField(blank=True, max_length=255)),
                ('profile_picture', models.CharField(blank=True, max_length=255)),
                ('steem_name', models.CharField(blank=True, default='false', max_length=256)),
                ('steem', models.CharField(blank=True, default='false', max_length=1024)),
                ('smoke_name', models.CharField(blank=True, default='false', max_length=256)),
                ('smoke', models.CharField(blank=True, default='false', max_length=1024)),
                ('whaleshare_name', models.CharField(blank=True, default='false', max_length=256)),
                ('whaleshare', models.CharField(blank=True, default='false', max_length=1024)),
                ('bitshare', models.CharField(blank=True, default='', max_length=1024, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
