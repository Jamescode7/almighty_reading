# Generated by Django 4.0.4 on 2022-05-27 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_membertopiclog_stage_membertopiclog_step_plan_stage1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanFlow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_code', models.IntegerField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='memberplanmanage',
            name='plan_code',
        ),
        migrations.DeleteModel(
            name='MemberLevelManage',
        ),
        migrations.DeleteModel(
            name='MemberPlanManage',
        ),
    ]
