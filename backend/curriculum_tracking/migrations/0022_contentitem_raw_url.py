# Generated by Django 3.1.4 on 2023-03-16 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum_tracking', '0021_auto_20230309_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentitem',
            name='raw_url',
            field=models.URLField(blank=True, max_length=2083, null=True, unique=True),
        ),
    ]