# Generated by Django 4.0.4 on 2022-09-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_reportcardmemo'),
    ]

    operations = [
        migrations.AddField(
            model_name='plandetail',
            name='step_mobile',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]