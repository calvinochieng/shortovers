from django.urls import path
from app.views import write,speech, voice
urlpatterns = [
    path('write/',write,name = "write"),
    path("speech/", speech, name="speech"),
    path('voice/', voice, name="voice"),
]