from django.db import models

# Create your models here.


class Level(models.Model):
    level_code = models.IntegerField(blank=True, null=True)
    level_name = models.CharField(max_length=30, blank=True, null=True)
    memo = models.CharField(max_length=20, null=True, blank=True)
    use_yn = models.CharField(max_length=1, null=True, blank=True)
    index_order = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    show_level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.level_name


class Theme(models.Model):
    theme_code = models.IntegerField(null=True, blank=True)
    level_code = models.IntegerField(null=True, blank=True)
    theme_name = models.CharField(max_length=30, null=True, blank=True)
    memo = models.CharField(max_length=20, null=True, blank=True)
    use_yn = models.CharField(max_length=1, null=True, blank=True)
    ord = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.theme_name)


class Topic(models.Model):
    theme_code = models.IntegerField()
    topic_code = models.IntegerField()
    topic_name = models.CharField(max_length=50, null=True, blank=True)
    pre_value = models.IntegerField(null=True, blank=True)
    use_yn = models.CharField(max_length=1, null=True, blank=True)
    ord = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.topic_name


class Word(models.Model):
    word_code = models.IntegerField()
    topic_code = models.IntegerField()
    page_num = models.IntegerField()
    num = models.IntegerField(null=True, blank=True)
    eng = models.CharField(max_length=100, null=True, blank=True)
    kor = models.CharField(max_length=100, null=True, blank=True)
    dic_eng = models.CharField(max_length=100, null=True, blank=True)
    dic_kor = models.CharField(max_length=100, null=True, blank=True)
    sound = models.CharField(max_length=100, null=True, blank=True)
    use_yn = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return str(self.eng) + '(' + str(self.kor) + ')'


class WrtMoon(models.Model):
    reading_code = models.IntegerField(null=True, blank=True)
    topic_code = models.IntegerField(null=True, blank=True)
    page_num = models.IntegerField(null=True, blank=True)
    para_num = models.IntegerField(null=True, blank=True)
    eng = models.CharField(max_length=8000, null=True, blank=True)
    kor = models.CharField(max_length=8000, null=True, blank=True)

    def __str__(self):
        return self.eng + ' / ' + self.kor


class WrtWord(models.Model):
    topic_code = models.IntegerField(null=True, blank=True)
    num = models.IntegerField(null=True, blank=True)
    eng = models.CharField(max_length=1000, null=True, blank=True)
    kor = models.CharField(max_length=1000, null=True, blank=True)
    sound = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.eng + ' / ' + self.kor


class Reading(models.Model):
    reading_code = models.IntegerField()
    topic_code = models.IntegerField(null=True, blank=True)
    page_num = models.IntegerField(null=True, blank=True)
    para_num = models.IntegerField(null=True, blank=True)
    eng = models.CharField(max_length=8000, null=True, blank=True)
    kor = models.CharField(max_length=8000, null=True, blank=True)
    sound = models.CharField(max_length=128, null=True, blank=True)
    rec_time = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.eng or 'None'


class ReadingPic(models.Model):
    topic_code = models.IntegerField()
    page_num = models.IntegerField(null=True, blank=True)
    pic = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.pic


class SpkSent(models.Model):
    topic_code = models.IntegerField()
    num = models.IntegerField(null=True, blank=True)
    eng = models.CharField(max_length=500, null=True, blank=True)
    kor = models.CharField(max_length=500, null=True, blank=True)
    sound = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.eng + ' / ' + self.kor


class Exam(models.Model):
    topic_code = models.IntegerField()
    num = models.IntegerField(null=True, blank=True)
    para_num = models.CharField(max_length=128, null=True, blank=True)
    kind = models.CharField(max_length=1, null=True, blank=True)
    ask = models.CharField(max_length=512, null=True, blank=True)
    answer = models.CharField(max_length=1, null=True, blank=True)
    s1 = models.CharField(max_length=255, null=True, blank=True)
    s2 = models.CharField(max_length=255, null=True, blank=True)
    s3 = models.CharField(max_length=255, null=True, blank=True)
    s4 = models.CharField(max_length=255, null=True, blank=True)
    s5 = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ask or 'None'
