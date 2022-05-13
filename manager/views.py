import random

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import date, timedelta

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from library.models import Level, Topic, SpkSent, Theme, Exam
from manager.models import Plan, MemberTopicLog
from member_info.models import TestMember


def manager_list(request):
    member_list = TestMember.objects.filter(acode='C72240')
    context = {
        'member_list': member_list,
    }
    return render(request, 'manager/manager_list.html', context)


def comprehension(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('topic code')

    exam_info = Exam.objects.filter(topic_code=topic_code)

    context = {
        'exam_info': exam_info,
    }
    return render(request, 'manager/comprehension.html', context)


def print_page(request):
    level_code = ''
    theme_code = ''
    theme_list = []
    topic_list = []

    if request.GET.get('lv'):
        level_code = request.GET.get('lv')
        theme_list = Theme.objects.filter(level_code=level_code)

    if request.GET.get('th'):
        theme_code = request.GET.get('th')
        topic_list = Topic.objects.filter(theme_code=theme_code)

    level_list = Level.objects.all()

    context = {
        'level_list': level_list,
        'theme_list': theme_list,
        'topic_list': topic_list,
        'level_code': level_code,  # eng, kor, eng+kor
        'theme_code': theme_code,
    }
    return render(request, 'manager/print.html', context)

def answer_page(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('topic code')

    exam_info = Exam.objects.filter(topic_code=topic_code)

    context = {
        'exam_info': exam_info,
    }
    return render(request, 'manager/answer.html', context)

def interpretation(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('topic code')

    both = 'both'
    if request.GET.get('type'):
        both = request.GET.get('type')

    random = 'normal'
    if request.GET.get('random'):
        random = request.GET.get('random')

    topic_info = Topic.objects.get(topic_code=topic_code)
    theme_info = Theme.objects.get(theme_code=topic_info.theme_code)
    level_info = Level.objects.get(level_code=theme_info.level_code)

    if random == 'normal':
        sentence_list = SpkSent.objects.filter(topic_code=topic_code)
    else:
        sentence_list = SpkSent.objects.filter(topic_code=topic_code).order_by('?')

    context = {
        'level_info': level_info,
        'theme_info': theme_info,
        'topic_info': topic_info,
        'both': both, #eng, kor, eng+kor
        'random': random,
        'sentence_list': sentence_list,
    }
    return render(request, 'manager/interpretation.html', context)


def main(request, user_id=''):
    is_select_level = False
    select_level_name = ''
    select_plan_name = ''
    user_name = ''
    level_list = []
    plan_list = []
    member_topic_log = []
    is_desc = 1
    desc = ''

    order_by = 'id'
    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')
        if request.GET.get('desc') == '1':
            is_desc = 0
        else:
            is_desc = 1
            desc = '-'

    member_list = TestMember.objects.filter(acode='C72240').order_by(desc+order_by)

    user = TestMember.objects.filter(mcode=user_id)
    if user:
        is_select_level = True
        user = user[0]
        if request.GET.get('mem_level'):
            mem_level = request.GET.get('mem_level')
            mem_plan = request.GET.get('mem_plan')
            user.level_code = Level.objects.get(level_code=mem_level)
            user.plan_code = Plan.objects.get(plan_code=mem_plan)
            user.save()
            return HttpResponseRedirect(reverse('manager:main', args=(user_id,)))

        level_list = Level.objects.all()
        select_level_name = str(user.level_code)
        select_plan_name = str(user.plan_code)
        plan_list = Plan.objects.all().order_by('-id')
        user_name = user.mname
        member_topic_log = MemberTopicLog.objects.filter(username=user_id)

    else:
        user_id = ''


    context = {
        'isDesc': is_desc,
        'isSelectLevel': is_select_level,
        'select_level_name': select_level_name,
        'select_plan_name': select_plan_name,
        'member_list': member_list,
        'level_list': level_list,
        'plan_list': plan_list,
        'user_name': user_name,
        'user_id': user_id,
        'member_topic_log':member_topic_log,
    }
    return render(request, 'manager/main.html', context)


def week(request):
    if request.GET.get('start_dt'):
        start_dt = request.GET.get('start_dt')
    else:
        start_dt = date.today()

    str = "This is python."
    print(str.strip()[-1])

    days = []
    loop = 6;
    for n in range(7):
        seek = loop - n
        day = start_dt - timedelta(seek)
        day_str = day.strftime('%m.%d') + getDay(day.weekday())
        print(day_str.strip()[-1])
        days.append(day_str)



    member_list = TestMember.objects.filter(acode='C72240')

    context = {
        'start_dt': start_dt,
        'days': days,
        'member_list': member_list,
    }
    return render(request, 'manager/week.html', context)


def getDay(num):
  switcher = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
  return switcher.get(num, "Please enter number between 1-7")




def dashboard(request):
    return render(request, 'manager/dashboard.html')


def basic_table(request):
    return render(request, 'manager/basic-table.html')


def profile(request):
    return render(request, 'manager/profile.html')


