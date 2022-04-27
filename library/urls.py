from django.urls import path

from library.views import LevelListView, TopicListView, ThemeListView, topic_view

app_name = 'library'

urlpatterns = [
    path('level/', LevelListView.as_view(), name='level_list'),
    path('theme/<int:level_code>', ThemeListView.as_view(), name='theme_list'),
    path('topic/<int:theme_code>', TopicListView.as_view(), name='topic_list'),
    path('topic_view/<int:topic_code>', topic_view, name='topic_view'),
]
