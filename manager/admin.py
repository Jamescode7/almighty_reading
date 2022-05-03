from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportMixin

from manager.models import MemberLevelManage, Plan, MemberPlanManage, MemberTopicLog


class MemberLevelManageAdmin(ImportExportMixin, admin.ModelAdmin ):
    pass

class PlanAdmin(ImportExportMixin, admin.ModelAdmin ):
    pass

class MemberPlanManageAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

class MemberTopicLogAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(MemberLevelManage, MemberLevelManageAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(MemberPlanManage, MemberPlanManageAdmin)
admin.site.register(MemberTopicLog, MemberTopicLogAdmin)