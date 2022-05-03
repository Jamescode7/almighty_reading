from django.contrib.auth.models import User
from django.db import models

from library.models import Level
from manager.models import Plan


class ZCenter(models.Model):
    code = models.CharField(max_length=6, null=True)
    btype = models.CharField(max_length=20, null=True)
    ctype = models.CharField(max_length=20, null=True)
    cname = models.CharField(max_length=255, null=True)
    ukey = models.IntegerField(max_length=10, null=True)
    uname = models.CharField(max_length=32, null=True)
    pkey = models.IntegerField(max_length=10, null=True)
    pname = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '(' + str(self.code) + ')' + str(self.uname)


class ZMember(models.Model):
    mcode = models.IntegerField(max_length=10, null=True)
    acode = models.CharField(max_length=6, null=True)
    mname = models.CharField(max_length=10, null=True)
    webid = models.CharField(max_length=20, null=True)
    mkind = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=6, null=True)


class TestAgency(models.Model):
    acode = models.CharField(max_length=10, null=True)
    aname = models.CharField(max_length=30, null=True)
    aman = models.CharField(max_length=10, null=True)
    webid = models.CharField(max_length=10, null=True)
    wcode = models.CharField(max_length=10, null=True)
    akind = models.CharField(max_length=10, null=True)
    bonbuacode = models.CharField(max_length=10, null=True)
    analkind = models.CharField(max_length=10, null=True)
    busikind = models.CharField(max_length=10, null=True)
    typekind = models.CharField(max_length=10, null=True)
    zonekind = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '(' + str(self.acode) + ')' + str(self.aname) + '(' + str(self.webid) + ')'


class TestMember(models.Model):
    mcode = models.CharField(max_length=10, null=True)
    mname = models.CharField(max_length=10, null=True)
    mtype = models.CharField(max_length=10, null=True)
    acode = models.CharField(max_length=10, null=True)
    plan_code = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.mcode) + ')' + str(self.mname) + '(' + str(self.mtype) + ')'
