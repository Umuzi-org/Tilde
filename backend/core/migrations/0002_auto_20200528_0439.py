# Generated by Django 2.1.5 on 2020-05-28 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cohort',
            name='suppress_card_generation',
            field=models.BooleanField(default=False),
        ),
    ]
