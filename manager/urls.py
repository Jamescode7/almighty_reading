from django.urls import path

from appapi.views import flash_version_check
from manager.views import dashboard, basic_table, profile, interpretation,\
    comprehension, week, week_up, print_page, answer_page, WeekListView, info, agency,  \
    downapp, day, plan_info, reportcard, plan_view, reportall, reportSelect, btns, test, test2

app_name = "manager"

urlpatterns = [
    path('FlashVersionCheck/', flash_version_check, name='FlashVersionCheck'),

    path('btns/', btns, name='btns'),
    path('btns/<str:code>', btns, name='btns'),

    path('info/', info, name='info'),
    path('info/<str:user_id>', info, name='info'),

    path('agency/', agency, name='agency'),
    path('agency/<str:agency_id>', agency, name='agency'),

    path('week/', week, name='week'),
    path('week/<int:prev_dt>', week, name='week'),

    path('week_up/', week_up, name='week_up'),
    path('week_up/<int:prev_dt>', week_up, name='week_up'),

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
    path('report_select/', reportSelect, name='report_select'),

    path('print/', print_page, name='print'),

    path('answer/', answer_page, name='answer'),
    path('answer/<str:topic_code>', answer_page, name='answer'),


    # html sample test view
    path('dashboard/', dashboard, name='dashboard'),
    path('basic_table/', basic_table, name='basic_table'),
    path('profile/', profile, name='profile'),


    # path('test/', test, name='test'),
    # path('test2/', test2, name='test2'),
]