from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student
# Register your models here.

class StudentAdmin(ImportExportModelAdmin):
    search_fields = ["pk"]
    list_display = [
        "pk",
        "student_id",
        "name",
        "Class_id",
        "is_delete"
    ]

admin.site.register(Student,StudentAdmin)

