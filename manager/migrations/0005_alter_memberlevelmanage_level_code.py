# Generated by Django 4.0.3 on 2022-05-02 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_memberlevelmanage_level_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberlevelmanage',
            name='level_code',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
    ]
