# Generated by Django 4.0.4 on 2022-05-30 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member_info', '0009_alter_studymember_plan_code_and_more'),
        ('manager', '0012_plandetail_delete_planflow_remove_plan_stage1_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Plan',
        ),
    ]
