# Generated by Django 2.1.5 on 2019-01-30 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threadedcomments', '0003_threadedcomment_newest_activity'),
        ('comments', '0002_auto_20190129_0633'),
    ]

    operations = [
        migrations.CreateModel(
            name='commentLD',
            fields=[
                ('threadedcomment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='threadedcomments.ThreadedComment')),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('LDcomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_comment', to='threadedcomments.ThreadedComment')),
                ('LDuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'abstract': False,
                'ordering': ('submit_date',),
                'permissions': [('can_moderate', 'Can moderate comments')],
            },
            bases=('threadedcomments.threadedcomment',),
        ),
    ]