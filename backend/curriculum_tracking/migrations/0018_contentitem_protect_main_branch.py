# Generated by Django 3.1.4 on 2022-06-02 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum_tracking', '0017_burndownsnapshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentitem',
            name='protect_main_branch',
            field=models.BooleanField(default=True),
        ),
    ]
