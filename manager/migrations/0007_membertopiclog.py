# Generated by Django 4.0.3 on 2022-05-02 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_level_level_code_alter_level_level_name'),
        ('manager', '0006_alter_memberlevelmanage_level_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberTopicLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=25, null=True)),
                ('start_dt', models.DateTimeField(auto_now=True, null=True)),
                ('end_dt', models.DateTimeField(auto_now=True, null=True)),
                ('level_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.level')),
                ('topic_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='library.topic')),
            ],
        ),
    ]
