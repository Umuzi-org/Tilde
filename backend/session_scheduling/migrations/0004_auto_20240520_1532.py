# Generated by Django 3.1.4 on 2024-05-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session_scheduling', '0003_session_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='extra_title_text',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
