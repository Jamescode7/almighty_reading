from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from library.models import Level, Theme, Topic, Word, WrtMoon, WrtWord, SpkSent, Exam, Reading


def bin_response(request):
    return HttpResponse('bin_response')


class LevelListView(ListView):
    model = Level
    context_object_name = 'level_list'
    template_name = 'library/level_list.html'
    paginate_by = 100


class ThemeListView(ListView):
    model = Theme
    context_object_name = 'theme_list'
    template_name = 'library/theme_list.html'

    def get_queryset(self):
        level_code = self.kwargs['level_code']
        return Theme.objects.filter(level_code=level_code)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topic_list'
    template_name = 'library/topic_list.html'

    def get_queryset(self):
        theme_code = self.kwargs['theme_code']
        return Topic.objects.filter(theme_code=theme_code)


def topic_view(request, topic_code):
    topic_name = Topic.objects.filter(topic_code=topic_code)[0]
    word_list = Word.objects.filter(topic_code=topic_code)
    sentence_list = SpkSent.objects.filter(topic_code=topic_code)
    para_list = Reading.objects.filter(topic_code=topic_code)
    row_list = []

    for para in para_list:
        #print(para.eng)
        para.eng = para.eng.replace('[', '')
        para.eng = para.eng.replace(']', '')
        para.eng = para.eng.replace('{', '')
        para.eng = para.eng.replace('}', '')
        para.eng = para.eng.replace('^', '\n')

        para.kor = para.kor.replace('^', '\n')
        para.kor = para.kor.replace('{', '')
        para.kor = para.kor.replace('}', '')

    context = {
        'sound_path': 'http://fmn2.tongclass.com/reading/data/',
        'topic_name': topic_name,
        'word_list': word_list,
        'sentence_list': sentence_list,
        'para_list': para_list,
    }
    return render(request, 'library/topicview.html', context)