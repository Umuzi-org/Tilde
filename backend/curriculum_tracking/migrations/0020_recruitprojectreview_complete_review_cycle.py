# Generated by Django 3.1.4 on 2022-09-20 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum_tracking', '0019_auto_20220809_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruitprojectreview',
            name='complete_review_cycle',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
