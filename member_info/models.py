from django.contrib.auth.models import User
from django.db import models

from library.models import Level
from manager.models import Plan


class TestMember(models.Model):
    mcode = models.CharField(max_length=10, null=True)
    mname = models.CharField(max_length=10, null=True)
    mtype = models.CharField(max_length=10, null=True)
    acode = models.CharField(max_length=10, null=True)
    plan_code = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True, default=2)
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.mcode) + ')' + str(self.mname) + '(' + str(self.mtype) + ')'


class StudyMember(models.Model):
    mcode = models.CharField(max_length=30, null=True)
    mname = models.CharField(max_length=30, null=True)
    # 예) c타입 웹전산에서 가져오기에 저장을 하긴 하지만 일단 사용 x
    mtype = models.CharField(max_length=10, null=True)
    # 학원 (agency) 코드
    acode = models.CharField(max_length=10, null=True)
    # 기본값 자유 = 2,   완전학습 = 1
    plan_code = models.ForeignKey(Plan, on_delete=models.PROTECT, null=True, blank=True, default=2)
    # level_code는 Level Model에 코드를 가지고 있지만. 그 용도는 레벨 제한이다.
    level_code = models.ForeignKey(Level, on_delete=models.PROTECT, null=True, blank=True)
    current_study = models.IntegerField(max_length=10, null=True, blank=True)
    def __str__(self):
        return '(' + str(self.mcode) + ')' + str(self.mname) + '(' + str(self.mtype) + ')'