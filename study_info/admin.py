from django.contrib import admin
from import_export.admin import ImportExportMixin

# Register your models here.
from study_info.models import TopicLog, StepFinishLog, StepTimeLog


class TopicLogAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class StepFinishLogAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class StepTimeLogAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

admin.site.register(TopicLog, TopicLogAdmin)
admin.site.register(StepFinishLog, StepFinishLogAdmin)
admin.site.register(StepTimeLog, StepTimeLogAdmin)