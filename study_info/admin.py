from django.contrib import admin
from import_export.admin import ImportExportMixin

# Register your models here.
from study_info.models import StepFinishLog, StepTimeLog


@admin.register(StepFinishLog)
class StepFinishLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'stage', 'step', 'step_num', 'dt_day', 'finish_today', 'plan_type', 'study_code']
    list_display_links = ['id']
    list_editable = ['stage', 'step', 'step_num', 'dt_day', 'finish_today', 'plan_type', 'study_code']


@admin.register(StepTimeLog)
class StepTimeLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'username', 'topic_code', 'step_code', 'study_time', 'step_dt']
    list_display_links = ['id']
    list_editable = ['username', 'topic_code', 'step_code', 'study_time']




