from django.db import models

# Create your models here.
from library.models import Level, Topic


class Plan(models.Model):
    plan_code = models.IntegerField(max_length=3, null=True, blank=True)
    plan_name = models.CharField(max_length=25, null=True, blank=True)
    stage1 = models.CharField(max_length=25, null=True, blank=True)
    stage2 = models.CharField(max_length=25, null=True, blank=True)
    stage3 = models.CharField(max_length=25, null=True, blank=True)
    stage4 = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.plan_name


class PlanFlow(models.Model):
    plan_code = models.IntegerField(max_length=3, null=True, blank=True)


class MemberTopicLog(models.Model):
    username = models.CharField(max_length=25, null=True, blank=True)
    topic_code = models.ForeignKey(Topic, on_delete=models.PROTECT, blank=True, null=True)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, blank=True, null=True)
    start_dt = models.DateTimeField(null=True, blank=True)
    end_dt = models.DateTimeField(null=True, blank=True)
    stage = models.IntegerField(max_length=3, null=True, blank=True)
    step = models.IntegerField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.username + '/' + str(self.topic_code) + '/' + str(self.level_code) + '/' + str(self.start_dt) + '/' + str(self.end_dt)