# Generated by Django 4.0.4 on 2022-06-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member_info', '0013_alter_studymember_current_study'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymember',
            name='acode',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='testmember',
            name='acode',
            field=models.CharField(max_length=50, null=True),
        ),
    ]