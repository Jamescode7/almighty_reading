from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from member_info.models import TestMember, StudyMember


class StudyMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TestMemberAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(StudyMember, StudyMemberAdmin)
admin.site.register(TestMember, TestMemberAdmin)


