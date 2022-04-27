from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from member_info.models import ZCenter, ZMember


class ZCenterAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ZMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(ZCenter, ZCenterAdmin)
admin.site.register(ZMember, ZMemberAdmin)