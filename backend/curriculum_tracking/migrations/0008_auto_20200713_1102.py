# Generated by Django 2.1.5 on 2020-07-13 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum_tracking', '0007_auto_20200710_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitprojectreview',
            name='status',
            field=models.CharField(choices=[('NYC', 'not yet competent'), ('C', 'competent'), ('E', 'excellent'), ('R', 'red flag')], default='NYC', max_length=3),
            preserve_default=False,
        ),
    ]
