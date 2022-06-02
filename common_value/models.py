from django.db import models

# Create your models here.


class AppVersion(models.Model):
    app_version = models.CharField(max_length=20, null=True)
    download_url = models.CharField(max_length=100, null=True)
    create_at = models.DateField(auto_created=True, null=True)

    def __str__(self):
        return self.app_version


class CommonCode(models.Model):
    code = models.CharField(max_length=10, null=True)
    code_name = models.CharField(max_length=50, null=True)
    up_code = models.CharField(max_length=10, null=True)
    code_value = models.CharField(max_length=50, null=True)
    ord = models.IntegerField(null=True)
    remark = models.CharField(max_length=100, null=True)
    mcode = models.IntegerField(null=True)
    code_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.code + '(' + self.code_name + ')'


class Step(models.Model):
    step_code = models.IntegerField(default=0)
    app_idx = models.IntegerField(default=0)
    step_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return '(' + str(self.app_idx) + ') ' + self.step_name


class EtcValue(models.Model):
    etc_name = models.CharField(max_length=50, null=True, blank=True)
    etc_value = models.CharField(max_length=50, null=True, blank=True)