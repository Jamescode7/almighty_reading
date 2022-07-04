from django.contrib import admin

# Register your models here.
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportMixin

from library.models import Topic, Level
from manager.models import MemberTopicLog, Plan, PlanDetail, ReportCardMemo


@admin.register(Plan)
class PlanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'plan_code', 'plan_name', 'seq']
    list_display_links = ['id']
    list_editable = ['plan_code', 'plan_name', 'seq']


@admin.register(PlanDetail)
class PlanAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'plan_code', 'seq', 'stage', 'step']
    list_display_links = ['id']
    list_editable = ['plan_code', 'seq', 'stage', 'step']


class MemberTopicLogResource(resources.ModelResource):
    topic_code = fields.Field(
        column_name='topic_code',
        attribute='topic_code',
        widget=ForeignKeyWidget(Topic, 'id')
    )
    level_code = fields.Field(
        column_name='level_code',
        attribute='level_code',
        widget=ForeignKeyWidget(Level, 'id')
    )

    class Meta:
        model = MemberTopicLog


@admin.register(MemberTopicLog)
class MemberTopicLogAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'username', 'topic_code', 'level_code', 'start_dt', 'end_dt', 'stage', 'step']
    list_display_links = ['username']
    list_editable = ['topic_code', 'level_code', 'start_dt', 'end_dt', 'stage', 'step']
    resource_class = MemberTopicLogResource


@admin.register(ReportCardMemo)
class ReportCardMemoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'seq', 'visible', 'title', 'memo']
    list_display_links = ['id']
    list_editable = ['seq', 'visible', 'title', 'memo']
