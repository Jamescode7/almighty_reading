from django.contrib import admin
from import_export.admin import ImportExportMixin


# Register your models here.
from library.models import Level, Theme, Topic, Word, WrtMoon, WrtWord, Reading, ReadingPic, SpkSent, Exam


@admin.register(Level)
class LevelAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'level_code', 'level_name', 'memo', 'use_yn', 'index_order', 'total']
    list_display_links = ['id']
    list_editable = ['level_code', 'level_name', 'memo', 'use_yn', 'index_order', 'total']


@admin.register(Theme)
class ThemeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'theme_code', 'level_code', 'theme_name', 'memo', 'use_yn', 'ord', 'total']
    list_display_links = ['id']
    list_editable = ['theme_code', 'level_code', 'theme_name', 'memo', 'use_yn', 'ord', 'total']


@admin.register(Topic)
class TopicAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'theme_code', 'topic_code', 'topic_name', 'pre_value', 'use_yn', 'ord']
    list_display_links = ['id']
    list_editable = ['theme_code', 'topic_code', 'topic_name', 'pre_value', 'use_yn', 'ord']


@admin.register(Word)
class WordAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'word_code', 'topic_code', 'page_num', 'num', 'eng', 'kor', 'dic_eng', 'dic_kor', 'sound',
                    'use_yn']
    list_display_links = ['id']
    list_editable = ['word_code', 'topic_code', 'page_num', 'num', 'eng', 'kor', 'dic_eng', 'dic_kor', 'sound',
                     'use_yn']


@admin.register(WrtMoon)
class WrtMoonAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'reading_code', 'topic_code', 'page_num', 'para_num', 'eng','kor']
    list_display_links = ['id']
    list_editable = ['reading_code', 'topic_code', 'page_num', 'para_num', 'eng','kor']


@admin.register(WrtWord)
class WrtWordAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'topic_code', 'num', 'eng', 'kor', 'sound']
    list_display_links = ['id']
    list_editable = ['topic_code', 'num', 'eng', 'kor', 'sound']


@admin.register(Reading)
class ReadingAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'reading_code', 'topic_code', 'page_num', 'para_num', 'eng', 'kor', 'sound', 'rec_time']
    list_display_links = ['id']
    list_editable = ['reading_code', 'topic_code', 'page_num', 'para_num', 'eng', 'kor', 'sound', 'rec_time']


@admin.register(ReadingPic)
class ReadingPicAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'topic_code', 'page_num', 'pic']
    list_display_links = ['id']
    list_editable = ['topic_code', 'page_num', 'pic']


@admin.register(SpkSent)
class SpkSentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'topic_code', 'num', 'eng', 'kor', 'sound']
    list_display_links = ['id']
    list_editable = ['topic_code', 'num', 'eng', 'kor', 'sound']


@admin.register(Exam)
class ExamAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'topic_code', 'num', 'para_num', 'kind', 'ask', 'answer', 's1', 's2', 's3', 's4', 's5']
    list_display_links = ['id']
    list_editable = ['topic_code', 'num', 'para_num', 'kind', 'ask', 'answer', 's1', 's2', 's3', 's4', 's5']









