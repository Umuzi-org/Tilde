# Generated by Django 3.1.4 on 2024-04-17 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_stream_flavours'),
        ('selection_bootcamps', '0002_provisionalgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='provisionalgroup',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='provisionalgroup',
            name='group_type',
            field=models.CharField(choices=[('Bridge', 'Bridge'), ('Prov accepted', 'Prov accepted')], default='Bridge', max_length=14),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provisionalgroup',
            name='paid',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provisionalgroup',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='provisionalgroup',
            name='stream',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.stream'),
            preserve_default=False,
        ),
    ]