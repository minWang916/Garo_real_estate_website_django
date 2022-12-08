from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    path('register/',signup_login, name='signup_login'),     
    path('logout/',log_out, name='log_out'),     
    path('profile/',profile, name='profile'),
    path('user-properties', user_properties, name = 'user_properties'),
    path('submit/',submit, name='submit'),
]
