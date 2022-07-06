from django.urls import path

from dialog.views import main, audio

app_name = "dialog"

urlpatterns = [
    path('', main, name='main'),
    path('main/', main, name='main'),
    path('audio/', audio, name='audio'),
]