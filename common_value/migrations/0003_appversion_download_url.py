# Generated by Django 4.0.3 on 2022-04-15 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_value', '0002_commoncode'),
    ]

    operations = [
        migrations.AddField(
            model_name='appversion',
            name='download_url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
