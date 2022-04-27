from django.contrib import admin
from import_export.admin import ImportExportMixin


# Register your models here.
from library.models import Level, Theme, Topic, Word, WrtMoon, WrtWord, Reading, ReadingPic, SpkSent, Exam


class LevelAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ThemeAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class TopicAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Level, LevelAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Topic, TopicAdmin)


class WordAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class WrtMoonAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class WrtWordAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ReadingAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ReadingPicAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class SpkSentAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


class ExamAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Word, WordAdmin)
admin.site.register(WrtMoon, WrtMoonAdmin)
admin.site.register(WrtWord, WrtWordAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(ReadingPic, ReadingPicAdmin)
admin.site.register(SpkSent, SpkSentAdmin)
admin.site.register(Exam, ExamAdmin)





