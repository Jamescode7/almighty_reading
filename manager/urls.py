from django.urls import path, re_path

from appapi.views import user_info_load, flash_version_check, common_test, \
    levelThemeLoad, themeTopicLoad, topicSelectSave, topicMainLoad, speakSentLoad, writeWordLoad, compLoad, \
    oXnoteLoad, stepFinishSave, stepTimeSave
from manager.views import manager_list, dashboard, basic_table, main, profile, interpretation,\
    comprehension, week, print_page, answer_page

app_name = "manager"

urlpatterns = [
    path('FlashVersionCheck/', flash_version_check, name='FlashVersionCheck'),
    path('manager_list/', manager_list, name='manager_list'),

    path('main/', main, name='main'),
    path('main/<str:user_id>', main, name='main'),

    path('week/', week, name='week'),

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