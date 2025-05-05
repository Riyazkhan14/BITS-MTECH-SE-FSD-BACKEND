from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import CustomUser
# Register your models here.

class UserAdmin(ImportExportModelAdmin):
    search_fields = ["pk"]
    list_display = [
        "pk",
        "name",
        "user_role",
        "email",
        "mobile_no",
        "Updated_on"
    ]

admin.site.register(CustomUser,UserAdmin)