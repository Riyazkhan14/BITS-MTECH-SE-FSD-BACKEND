from django.urls import include, path
from class_app.views import *
from class_app.api_views import *

app_name = 'class_app'

urlpatterns = [

    path('all',all_classes,name='all_classes'),
]