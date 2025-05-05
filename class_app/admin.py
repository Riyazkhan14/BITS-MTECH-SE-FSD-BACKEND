from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Classes
# Register your models here.

class ClassesAdmin(ImportExportModelAdmin):
    search_fields = ["pk"]
    list_display = [
        "pk",
        "name",
        "is_delete"
    ]

admin.site.register(Classes,ClassesAdmin)
