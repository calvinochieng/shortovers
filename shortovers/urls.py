from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404, handler500
from app.views import *
from app import urls as appUrls

urlpatterns = [
    path('', index, name='index'), 
    path('',include('app.urls')),
    path('admin/', admin.site.urls), 

    path("user/register/", register, name="register"),
]

handler404 = error_404
handler500 = error_500