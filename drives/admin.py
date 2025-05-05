from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Vaccine_Drives,Students_Vaccination
# Register your models here.

class DriveAdmin(ImportExportModelAdmin):
    search_fields = ["pk"]
    list_display = [
        "pk",
        "vaccine_name",
        "Class_id",
        "drive_date",
        "available_slots",
        "is_delete"
    ]

admin.site.register(Vaccine_Drives,DriveAdmin)

class Students_VaccinationAdmin(ImportExportModelAdmin):
    search_fields = ["pk"]
    list_display = [
        "pk",
        "Vaccine_id",
        "Student_id",
        "vaccination_date"
    ]

admin.site.register(Students_Vaccination,Students_VaccinationAdmin)