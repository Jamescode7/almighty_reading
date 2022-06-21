from django.contrib import admin

# Register your models here.
from dialog.models import Dialog
from import_export.admin import ImportExportMixin

from dialog.models import Dialog


@admin.register(Dialog)
class LevelAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'step', 'book_cd', 'track']
    list_display_links = ['id']
    list_editable = ['name', 'step', 'book_cd', 'track']


