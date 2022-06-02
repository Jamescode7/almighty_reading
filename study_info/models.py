from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from library.models import Topic


class StepFinishLog(models.Model):
    username = models.CharField(max_length=25, null=True, blank=True)
    dt_year = models.CharField(max_length=3, null=True, blank=True)
    dt_month = models.CharField(max_length=3, null=True, blank=True)
    dt_day = models.CharField(max_length=3, null=True, blank=True)
    topic_code = models.CharField(max_length=10, null=True, blank=True)
    step_code = models.CharField(max_length=10, null=True, blank=True)
    step_num = models.CharField(max_length=3, null=True, blank=True)
    c_point = models.IntegerField(null=True, blank=True)
    t_point = models.IntegerField(null=True, blank=True)
    answer = models.CharField(max_length=25, null=True, blank=True)
    finish_dt = models.DateTimeField(auto_now=True, null=True)
    stage = models.IntegerField(null=True, blank=True)
    step = models.IntegerField(null=True, blank=True)
    plan_type = models.IntegerField(null=True, blank=True)
    study_code = models.IntegerField(null=True, blank=True)
    finish_today = models.IntegerField(null=True, blank=True, default=0)


class StepTimeLog(models.Model):
    username = models.CharField(max_length=25, null=True, blank=True)
    topic_code = models.CharField(max_length=10, null=True, blank=True)
    step_code = models.CharField(max_length=10, null=True, blank=True)
    study_time = models.CharField(max_length=25, null=True, blank=True)
    step_dt = models.DateTimeField(auto_now=True, null=True)

