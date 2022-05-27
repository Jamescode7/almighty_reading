from django.contrib import admin
from import_export.admin import ImportExportMixin

# Register your models here.
from study_info.models import StepFinishLog, StepTimeLog


@admin.register(StepFinishLog)
class StepFinishLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'username', 'dt_year', 'dt_month', 'dt_day', 'topic_code', 'step_code', 'step_num', 'c_point', 't_point', 'answer', 'finish_dt', 'stage', 'step', 'plan_type', 'study_code']
    list_display_links = ['id']
    list_editable = ['username', 'dt_year', 'dt_month', 'dt_day', 'topic_code', 'step_code', 'step_num', 'c_point', 't_point', 'answer', 'stage', 'step', 'plan_type', 'study_code']


@admin.register(StepTimeLog)
class StepTimeLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'username', 'topic_code', 'step_code', 'study_time', 'step_dt']
    list_display_links = ['id']
    list_editable = ['username', 'topic_code', 'step_code', 'study_time']




