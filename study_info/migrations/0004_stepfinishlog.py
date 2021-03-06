# Generated by Django 4.0.3 on 2022-04-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_info', '0003_delete_steplog'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepFinishLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=25, null=True)),
                ('topic_code', models.CharField(blank=True, max_length=10, null=True)),
                ('step_code', models.CharField(blank=True, max_length=10, null=True)),
                ('step_num', models.CharField(blank=True, max_length=25, null=True)),
                ('c_point', models.IntegerField(blank=True, max_length=10, null=True)),
                ('t_point', models.IntegerField(blank=True, max_length=10, null=True)),
                ('answer', models.CharField(blank=True, max_length=25, null=True)),
                ('finish_dt', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
