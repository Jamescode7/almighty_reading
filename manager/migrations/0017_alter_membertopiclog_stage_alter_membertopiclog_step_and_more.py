# Generated by Django 4.0.4 on 2022-05-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_alter_plandetail_plan_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membertopiclog',
            name='stage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='membertopiclog',
            name='step',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='plan_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plandetail',
            name='seq',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='plandetail',
            name='stage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]