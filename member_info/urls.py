from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from member_info.views import bin_response, bin_render, bin_padding, del_center, CenterListView, MemberListView, \
    MemberList2View

app_name = "member_info"

urlpatterns = [
    path('bin_response/', bin_response, name='bin_response'),
    path('bin_render/', bin_render, name='bin_render'),

    path('bin_padding/', bin_padding, name='bin_padding'),
    path('del_center/', del_center, name='del_center'),#엑셀 잘못 넣었을떄 삭제하려고 만듬.

    path('center_list/', CenterListView.as_view(), name='center_list'),
    path('member_list/', MemberList2View.as_view(), name='member_list'),
    path('center_member_list/', MemberListView.as_view(), name='center_member_list'),

]