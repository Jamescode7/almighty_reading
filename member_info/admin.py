from django.contrib import admin

# Register your models here.
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportMixin

from library.models import Level
from member_info.models import TestMember, StudyMember


class StudyMemberResource(resources.ModelResource):
    level_code = fields.Field(
        column_name='level_code',
        attribute='level_code',
        widget=ForeignKeyWidget(Level, 'id')
    )

    class Meta:
        model = StudyMember


@admin.register(StudyMember)
class StudyMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['mcode', 'mname', 'acode', 'plan_code', 'level_code', 'current_study', 'list_enable']
    list_display_links = ['mcode']
    list_editable = ['mname', 'acode', 'plan_code', 'level_code', 'current_study', 'list_enable']

    resource_class = StudyMemberResource


@admin.register(TestMember)
class TestMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'mcode', 'mname', 'mtype', 'acode', 'plan_code', 'level_code']
    list_display_links = ['id']
    list_editable = ['mcode', 'mname', 'mtype', 'acode', 'plan_code', 'level_code']