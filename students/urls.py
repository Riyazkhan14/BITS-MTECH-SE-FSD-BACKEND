from django.urls import include, path
from students.views import *
from students.api_views import *

app_name = 'students'

urlpatterns = [

    path('all_students',all_students,name='all_students'),

    path('add_student',add_student,name='add_student'),

    path('update_student/<int:pk>',update_student,name='update_student'),

    path('delete_student/<int:pk>',delete_student,name='delete_student'),

    path('upload',student_upload,name='student_upload'),

]
