from django.db import models

# Create your models here.


class Dialog(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    step = models.CharField(max_length=20, null=True, blank=True)
    book_cd = models.CharField(max_length=10, null=True, blank=True)
    track = models.IntegerField(null=True, blank=True)