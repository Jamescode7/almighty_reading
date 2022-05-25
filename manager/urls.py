from django.urls import path, re_path

from appapi.views import flash_version_check
from manager.views import dashboard, basic_table, main, profile, interpretation,\
    comprehension, week, print_page, answer_page, WeekListView, info, agency, test

app_name = "manager"

urlpatterns = [
    path('FlashVersionCheck/', flash_version_check, name='FlashVersionCheck'),

    # sample - dev
    path('main/', main, name='main'),
    path('main/<str:user_id>', main, name='main'),

    path('info/', info, name='info'),
    path('info/<str:user_id>', info, name='info'),

    path('agency/', agency, name='agency'),
    path('agency/<str:agency_id>', agency, name='agency'),

    path('week/', week, name='week'),


    #dev check
    path('week_dev/', WeekListView.as_view(), name='week_dev'),
    path('test/', test, name='test'),

    #paper
    path('interpretation/', interpretation, name='interpretation'),
    path('interpretation/<str:topic_code>', interpretation, name='interpretation'),

    path('comprehension/', comprehension, name='comprehension'),
    path('comprehension/<str:topic_code>', comprehension, name='comprehension'),

    path('print/', print_page, name='print'),

    path('answer/', answer_page, name='answer'),
    path('answer/<str:topic_code>', answer_page, name='answer'),


    # html sample test view
    path('dashboard/', dashboard, name='dashboard'),
    path('basic_table/', basic_table, name='basic_table'),
    path('profile/', profile, name='profile'),
]