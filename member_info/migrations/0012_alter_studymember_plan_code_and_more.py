# Generated by Django 4.0.4 on 2022-05-30 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0014_plan'),
        ('member_info', '0011_alter_studymember_plan_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymember',
            name='plan_code',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.plan'),
        ),
        migrations.AlterField(
            model_name='testmember',
            name='plan_code',
            field=models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.PROTECT, to='manager.plan'),
        ),
    ]