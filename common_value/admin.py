from django.contrib import admin
from import_export.admin import ImportExportMixin

# Register your models here.
from common_value.models import AppVersion, CommonCode


class AppVersionAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class CommonCodeAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(AppVersion, AppVersionAdmin)
admin.site.register(CommonCode, CommonCodeAdmin)