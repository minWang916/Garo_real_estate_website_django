from django.urls import path
from home.views import *

app_name = 'home'
urlpatterns = [
    path('',index, name='index'),    
    path('contact/',contact, name='contact'),   
    path('homes/',homes, name='homes'),  
    path('home/<int:id>/',property_single, name='home'),
    path('search/', search, name = "search"),
    path('edit/<int:id>', edit, name = "edit"),
    path('delete/<int:id>', delete, name = "delete"),
]
