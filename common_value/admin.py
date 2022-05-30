from django.contrib import admin
from import_export.admin import ImportExportMixin

# Register your models here.
from common_value.models import AppVersion, CommonCode, EtcValue, Step


@admin.register(AppVersion)
class AppVersionAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'app_version', 'download_url', 'create_at']
    list_display_links = ['id']
    list_editable = ['app_version', 'download_url', 'create_at']


@admin.register(CommonCode)
class CommonCodeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'code', 'code_name', 'up_code', 'code_value', 'ord', 'remark', 'mcode', 'code_date']
    list_display_links = ['id']
    list_editable = ['code', 'code_name', 'up_code', 'code_value', 'ord', 'remark', 'mcode']


@admin.register(EtcValue)
class EtcValueAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'etc_name', 'etc_value']
    list_display_links = ['id']
    list_editable = ['etc_name', 'etc_value']


@admin.register(Step)
class StepAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'step_code', 'app_idx', 'step_name']
    list_display_links = ['id']
    list_editable = ['step_code', 'app_idx', 'step_name']