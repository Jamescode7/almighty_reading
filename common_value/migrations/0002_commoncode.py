# Generated by Django 4.0.3 on 2022-04-14 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_value', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommonCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, null=True)),
                ('code_name', models.CharField(max_length=50, null=True)),
                ('up_code', models.CharField(max_length=10, null=True)),
                ('code_value', models.CharField(max_length=50, null=True)),
                ('ord', models.IntegerField(max_length=3, null=True)),
                ('remark', models.CharField(max_length=100, null=True)),
                ('mcode', models.IntegerField(max_length=10, null=True)),
                ('code_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
    ]
