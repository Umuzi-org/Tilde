# Generated by Django 3.1.4 on 2024-06-03 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_review_pricing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectreviewpricingscore',
            name='weight_share',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=4, null=True),
        ),
    ]