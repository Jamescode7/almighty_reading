from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from member_info.models import ZCenter, ZMember, TestAgency, TestMember


class ZCenterAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ZMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TestAgencyAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TestMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(ZCenter, ZCenterAdmin)
admin.site.register(ZMember, ZMemberAdmin)
admin.site.register(TestAgency, TestAgencyAdmin)
admin.site.register(TestMember, TestMemberAdmin)


