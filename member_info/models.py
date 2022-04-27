from django.contrib.auth.models import User
from django.db import models


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

