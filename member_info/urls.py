from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from member_info.views import bin_response, bin_render, bin_padding


app_name = "member_info"

urlpatterns = [
    #path('bin_response/', bin_response, name='bin_response'),
    #path('bin_render/', bin_render, name='bin_render'),
    #path('bin_padding/', bin_padding, name='bin_padding'),

]