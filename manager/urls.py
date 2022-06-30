from django.urls import path

from appapi.views import flash_version_check
from manager.views import dashboard, basic_table, profile, interpretation,\
    comprehension, week, print_page, answer_page, WeekListView, info, agency,  \
    downapp, day, plan_info, reportcard, plan_view, reportall

app_name = "manager"

urlpatterns = [
    path('FlashVersionCheck/', flash_version_check, name='FlashVersionCheck'),

    path('info/', info, name='info'),
    path('info/<str:user_id>', info, name='info'),

    path('agency/', agency, name='agency'),
    path('agency/<str:agency_id>', agency, name='agency'),

    path('week/', week, name='week'),
    path('week/<int:prev_dt>', week, name='week'),

    path('day/', day, name='day'),

    path('download/', downapp, name='downapp'),

    path('plan_info/', plan_info, name='plan_info'),
    path('plan_view/', plan_view, name='plan_view'),

    # path('call/', call, name='call'),


    #dev check
    path('week_dev/', WeekListView.as_view(), name='week_dev'),

    #paper
    path('interpretation/', interpretation, name='interpretation'),
    path('interpretation/<str:topic_code>', interpretation, name='interpretation'),

    path('comprehension/', comprehension, name='comprehension'),
    path('comprehension/<str:topic_code>', comprehension, name='comprehension'),

    path('reportcard/', reportcard, name='reportcard'),
    path('reportcard/<str:mcode>', reportcard, name='reportcard'),

    path('reportall/', reportall, name='reportall'),

    path('print/', print_page, name='print'),

    path('answer/', answer_page, name='answer'),
    path('answer/<str:topic_code>', answer_page, name='answer'),


    # html sample test view
    path('dashboard/', dashboard, name='dashboard'),
    path('basic_table/', basic_table, name='basic_table'),
    path('profile/', profile, name='profile'),
]