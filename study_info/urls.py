from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from study_info.views import bin_response

app_name = "study_info"

urlpatterns = [
    path('bin_response/', bin_response, name='bin_response'),

    path('list/', bin_response, name='list'),
    path('detail/', bin_response, name='detail'),
    path('monthly/', bin_response, name='bin_response'),


]