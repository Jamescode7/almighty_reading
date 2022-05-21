from django.contrib.auth.models import User
from django.db import models

from library.models import Level
from manager.models import Plan


class TestMember(models.Model):
    mcode = models.CharField(max_length=10, null=True)
    mname = models.CharField(max_length=10, null=True)
    mtype = models.CharField(max_length=10, null=True)
    acode = models.CharField(max_length=10, null=True)
    plan_code = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.mcode) + ')' + str(self.mname) + '(' + str(self.mtype) + ')'


class StudyMember(models.Model):
    mcode = models.CharField(max_length=30, null=True)
    mname = models.CharField(max_length=30, null=True)
    mtype = models.CharField(max_length=10, null=True)
    acode = models.CharField(max_length=10, null=True)
    plan_code = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.mcode) + ')' + str(self.mname) + '(' + str(self.mtype) + ')'