# Generated by Django 3.1.4 on 2024-06-10 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_review_pricing', '0002_auto_20240603_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectreviewpricingscore',
            name='weight_share',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True),
        ),
    ]