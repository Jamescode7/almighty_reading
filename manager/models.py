from django.db import models

# Create your models here.
from common_value.models import Step, StepMobile
from library.models import Level, Topic


class Plan(models.Model):
    plan_code = models.IntegerField(null=True, blank=True)
    plan_name = models.CharField(max_length=25, null=True, blank=True)
    seq = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.plan_name


class PlanDetail(models.Model):
    plan_code = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    stage = models.IntegerField(null=True, blank=True)
    step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    step_mobile = models.ForeignKey(StepMobile, on_delete=models.SET_NULL, null=True, blank=True)



class MemberTopicLog(models.Model):
    username = models.CharField(max_length=25, null=True, blank=True)
    topic_code = models.ForeignKey(Topic, on_delete=models.PROTECT, blank=True, null=True)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, blank=True, null=True)
    start_dt = models.DateTimeField(null=True, blank=True)
    end_dt = models.DateTimeField(null=True, blank=True)
    stage = models.IntegerField(null=True, blank=True)
    step = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username + '/' + str(self.topic_code) + '/' + str(self.level_code) + '/' + str(self.start_dt) + '/' + str(self.end_dt)


class ReportCardMemo(models.Model):
    seq = models.IntegerField(null=True, blank=True)
    visible = models.IntegerField(null=True, blank=True, default=1)
    title = models.CharField(max_length=100, null=True, blank=True)
    memo = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.seq) + '/' + self.title
