from django.urls import path

from appapi.views import user_info_load, flash_version_check, common_test, \
    levelThemeLoad, themeTopicLoad, topicSelectSave, topicMainLoad, speakSentLoad, writeWordLoad, compLoad, \
    oXnoteLoad, stepFinishSave, stepTimeSave

app_name = "appapi"

urlpatterns = [
    path('FlashVersionCheck/', flash_version_check, name='FlashVersionCheck'),
    path('UserInfoLoad/', user_info_load, name='UserInfoLoad'),#https://cem.mrzero.kr/rodata/ca/UserInfoLoad?Password=hello&UserID=cem&dummy=1650007104221
    path('CommonTest/', common_test, name='CommonTest'),#https://cem.mrzero.kr/rodata/ca/CommonTest?Time=457537&Mcode=26533

    # - LIBRARY
    path('LevelThemeLoad/', levelThemeLoad, name='LevelThemeLoad'),#https://cem.mrzero.kr/rodata/ca/LevelThemeLoad?Time=461871&Mcode=26533&Keyword=
    path('ThemeTopicLoad/', themeTopicLoad, name='ThemeTopicLoad'),#https://cem.mrzero.kr/rodata/ca/ThemeTopicLoad?Time=1716041&Mcode=26533&Tcode=110&Keyword=
    path('TopicSelectSave/', topicSelectSave, name='TopicSelectSave'), #https://cem.mrzero.kr/rodata/ca/TopicSelectSave?Time=3414637&Mcode=26533&Pcode=364
    path('TopicMainLoad/', topicMainLoad, name='TopicMainLoad'), #https://cem.mrzero.kr/rodata/ca/TopicMainLoad?Time=3415193&Mcode=26533&FlashCode=529647&Pcode=364
    path('SpeakSentLoad/', speakSentLoad, name='SpeakSentLoad'),#https://cem.mrzero.kr/rodata/ca/SpeakSentLoad?Time=4641057&Mcode=26533&Pcode=364
    path('WriteWordLoad/', writeWordLoad, name='WriteWordLoad'), #https://cem.mrzero.kr/rodata/ca/WriteWordLoad?Time=4768614&Mcode=26533&Pcode=364
    path('CompLoad/', compLoad, name='CompLoad'), #https://cem.mrzero.kr/rodata/ca/CompLoad?Time=5301995&Mcode=26533&Pcode=364
    path('OXnoteLoad', oXnoteLoad, name='OXnoteLoad'), #https://cem.mrzero.kr/rodata/ca/OXnoteLoad?Time=5564776&Mcode=26533&Pcode=364

    # - STUDY_INFO
    path('StepFinishSave/', stepFinishSave, name='StepFinishSave'), #https://cem.mrzero.kr/rodata/ca/StepFinishSave?Time=5169391&Mcode=26533&FlashCode=529647&Pcode=364&StepCode=P09&StepNum=0&Cpoint=0&Tpoint=0&Ans=null&StudyTime=24
    path('StepTimeSave/', stepTimeSave, name='StepTimeSave'), #https://cem.mrzero.kr/rodata/ca/StepTimeSave?Time=46989&Mcode=27462&Pcode=4136&FlashCode=410816&StudyTime=0&StepCode=P01
]