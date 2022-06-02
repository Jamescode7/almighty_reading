from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from manager.models import MemberTopicLog, Plan, PlanDetail


@admin.register(Plan)
class PlanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'plan_code', 'plan_name']
    list_display_links = ['id']
    list_editable = ['plan_code', 'plan_name']


@admin.register(PlanDetail)
class PlanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'plan_code', 'seq', 'stage', 'step']
    list_display_links = ['id']
    list_editable = ['plan_code', 'seq', 'stage', 'step']


@admin.register(MemberTopicLog)
class MemberTopicLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'username', 'topic_code', 'level_code', 'start_dt', 'end_dt', 'stage', 'step']
    list_display_links = ['username']
    list_editable = ['topic_code', 'level_code', 'start_dt', 'end_dt', 'stage', 'step']

