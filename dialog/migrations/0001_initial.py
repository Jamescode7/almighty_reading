# Generated by Django 4.0.4 on 2022-06-21 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('step', models.CharField(blank=True, max_length=20, null=True)),
                ('book_cd', models.CharField(blank=True, max_length=10, null=True)),
                ('track', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]