# Generated by Django 4.0.4 on 2022-09-22 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_value', '0012_stepmobile'),
        ('manager', '0021_remove_plandetail_step_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='plandetail',
            name='step_mobile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common_value.stepmobile'),
        ),
    ]
