from django.urls import include, path
from drives.views import *
from drives.api_views import *

app_name = 'drives'

urlpatterns = [

    path('all',all_drives,name='all_drives'),

    path('add',add_drive,name='add_drive'),

    path('update/<int:pk>',update_drive,name='update_drive'),

    path('delete/<int:pk>',delete_drive,name='delete_drive'),

    path('student_vaccine_data',student_vaccine_data,name='student_vaccine_data'),

    path('add_student_vaccine',add_student_vaccine,name='add_student_vaccine'),

    path('data_upload',student_vaccination_upload,name='student_vaccination_upload'),

    path('count_api',count_api,name='count_api'),

    path('vaccination_report',vaccination_report,name='vaccination_report'),

    path('export_vaccination_data',export_vaccination_data,name='export_vaccination_data'),

]