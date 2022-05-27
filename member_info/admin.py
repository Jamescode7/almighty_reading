from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from member_info.models import TestMember, StudyMember


@admin.register(StudyMember)
class StudyMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'mcode', 'mname', 'acode', 'plan_code', 'level_code', 'current_study']
    list_display_links = ['id']
    list_editable = ['mcode', 'mname', 'acode', 'plan_code', 'level_code', 'current_study']


@admin.register(TestMember)
class TestMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'mcode', 'mname', 'mtype', 'acode', 'plan_code', 'level_code']
    list_display_links = ['id']
    list_editable = ['mcode', 'mname', 'mtype', 'acode', 'plan_code', 'level_code']