from django.urls import include, path
from accounts.views import *
from accounts.api_views import *

app_name = 'accounts'

urlpatterns = [

    path('register',register_view,name='register_view'),

    path('login',login_api,name='login_api'),
]