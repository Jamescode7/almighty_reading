# Generated by Django 4.0.4 on 2022-05-30 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common_value', '0009_plan_step'),
        ('member_info', '0008_studymember_current_study_alter_studymember_mcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymember',
            name='plan_code',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='common_value.plan'),
        ),
        migrations.AlterField(
            model_name='testmember',
            name='plan_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common_value.plan'),
        ),
    ]