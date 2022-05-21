import random
import urllib
import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from library.models import Level, Topic, SpkSent, Theme, Exam
from manager.models import Plan, MemberTopicLog
from member_info.models import StudyMember
from study_info.models import StepFinishLog


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
        'both': both,  # eng, kor, eng+kor
        'random': random,
        'sentence_list': sentence_list,
    }
    return render(request, 'manager/interpretation.html', context)


def agency(request, agency_id=''):
    if agency_id == '':
        return HttpResponse('잘못된 접근입니다')
    else:
        aid = request.session['agency'] = agency_id
        # print('agency id : ' + aid)
        return HttpResponseRedirect(reverse('manager:info'))


def get_json_url(url):
    oper_url = urllib.request.urlopen(url)
    if oper_url.getcode() == 200:
        data = oper_url.read().decode(oper_url.headers.get_content_charset())
        json_data = json.loads(data)
    else:
        print("Error receiving data", oper_url.getcode())
    return json_data


def info(request, user_id=''):
    if 'agency' in request.session:
        aid = request.session['agency']
        print('agency id : ' + aid)
    else:
        return HttpResponse('잘못된 접근입니다')

    # 웹전산에서 정보 가져오기
    url = "http://www.tongclass.co.kr/Class/api_member.aspx?ac=" + aid
    json_data = get_json_url(url)

    for row in json_data:
        row_id = row['Id']
        row_name = row['Mn']
        #print(row_id + '/' + row_name)
        # 회원이 없다면 등록시키기.
        study_member = StudyMember.objects.filter(mcode=row_id)
        if study_member:
            if study_member[0].acode is None:
                study_member[0].acode = aid
                study_member.save()
        else:
            study_member = StudyMember(mcode=row_id, mname=row_name, acode=aid, plan_code=Plan.objects.get(plan_code=2))
            study_member.save()

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

    member_list = StudyMember.objects.filter(acode=aid).order_by(desc + order_by)

    user = StudyMember.objects.filter(mcode=user_id)
    if user:
        is_select_level = True
        user = user[0]

        # 플랜이나 레벨제한을 바꿨을때 실행.
        if request.GET.get('mem_level'):
            mem_level = request.GET.get('mem_level')
            mem_plan = request.GET.get('mem_plan')
            user.level_code = Level.objects.get(level_code=mem_level)
            user.plan_code = Plan.objects.get(plan_code=mem_plan)
            user.save()
            return HttpResponseRedirect(reverse('manager:main', args=(user_id,)))

        # 토픽 종료 또는 토픽 리셋 실행.
        if request.GET.get('process'):
            process = request.GET.get('process')
            process_id = request.GET.get('process_id')
            log = MemberTopicLog.objects.filter(id=process_id)
            if log:
                log = log[0]
                if process == 'closed':
                    log.end_dt = datetime.now()

                elif process == 'reset':
                    log.start_dt = datetime.now()
                    log.end_dt = None
                    log.stage = 1
                    log.step = 1
                log.save()

                return HttpResponseRedirect(reverse('manager:main', args=(user_id,)))

        level_list = Level.objects.all()
        select_level_name = str(user.level_code)
        select_plan_name = str(user.plan_code)
        plan_list = Plan.objects.all().order_by('-id')
        user_name = user.mname
        member_topic_log = MemberTopicLog.objects.filter(username=user_id).order_by('-id')


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
        'member_topic_log': member_topic_log,
    }
    return render(request, 'manager/info.html', context)


def main(request, user_id='', agency_id=''):
    print('agency_id : ' + agency_id)
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

    member_list = StudyMember.objects.filter(acode='C72240').order_by(desc + order_by)

    user = StudyMember.objects.filter(mcode=user_id)
    if user:
        is_select_level = True
        user = user[0]

        # 플랜이나 레벨제한을 바꿨을때 실행.
        if request.GET.get('mem_level'):
            mem_level = request.GET.get('mem_level')
            mem_plan = request.GET.get('mem_plan')
            user.level_code = Level.objects.get(level_code=mem_level)
            user.plan_code = Plan.objects.get(plan_code=mem_plan)
            user.save()
            return HttpResponseRedirect(reverse('manager:main', args=(user_id,)))

        # 토픽 종료 또는 토픽 리셋 실행.
        if request.GET.get('process'):
            process = request.GET.get('process')
            process_id = request.GET.get('process_id')
            log = MemberTopicLog.objects.filter(id=process_id)
            if log:
                log = log[0]
                if process == 'closed':
                    log.end_dt = datetime.now()

                elif process == 'reset':
                    log.start_dt = datetime.now()
                    log.end_dt = None
                    log.stage = 1
                    log.step = 1
                log.save()

                return HttpResponseRedirect(reverse('manager:main', args=(user_id,)))

        level_list = Level.objects.all()
        select_level_name = str(user.level_code)
        select_plan_name = str(user.plan_code)
        plan_list = Plan.objects.all().order_by('-id')
        user_name = user.mname
        member_topic_log = MemberTopicLog.objects.filter(username=user_id).order_by('-id')


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
        'member_topic_log': member_topic_log,
    }
    return render(request, 'manager/main.html', context)


class WeekListView(ListView):
    model = StepFinishLog
    context_object_name = 'week_list'
    template_name = 'manager/week_list_dev.html'
    ordering = '-id'


def daytest(request):
    today = date.today()
    year = today.strftime('%y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    print('year : ' + year)
    print('month : ' + month)
    print('day : ' + day)
    return HttpResponse('year : ' + year)


def week(request):
    if 'agency' in request.session:
        aid = request.session['agency']
        #print('agency id : ' + aid)
    else:
        return HttpResponse('잘못된 접근입니다')

    if request.GET.get('start_dt'):
        start_dt = request.GET.get('start_dt')
    else:
        start_dt = date.today()

    days = []
    loop = 6
    for n in range(7):
        seek = loop - n
        day = start_dt - timedelta(seek)
        day_str = day.strftime('%m.%d') + getDay(day.weekday())
        # print(day_str.strip()[-1])
        days.append(day_str)

    member_list = StudyMember.objects.filter(acode=aid)
    # 01 모든 학생을 가져온다.
    for member in member_list:
        member.days = []
        loop = 6
        # 02 한 학생당 지정된(seek) 날짜로부터 지난 7일간의 날짜를 가져온다.
        for dt in range(7):
            seek = loop - dt
            day = start_dt - timedelta(seek)
            day_str = day.strftime('%m.%d') + getDay(day.weekday())
            yy = day.strftime('%y')
            mm = day.strftime('%m')
            dd = day.strftime('%d')

            # 03 날짜당 학생의 데이터를 추출해본다.
            stepFinishLog = StepFinishLog.objects.filter(username=member.mcode, dt_year=yy, dt_month=mm, dt_day=dd)
            study_data = {}
            if stepFinishLog:
                study_data['st'] = ''
                study_data['st1'] = ''
                study_data['st2'] = ''
                study_data['st3'] = ''
                color_str = "gray"  # or blue
                for log in stepFinishLog:
                    # 04 stage별로 마지막까지 학습을 했다면 st-blue, 그렇지 않으면 st-gray
                    if log.stage == 1:
                        if log.step == 2:
                            color_str = "blue"
                    elif log.stage == 2:
                        if log.step == 2:
                            color_str = "blue"
                    elif log.stage == 3:
                        if log.step == 3:
                            if log.step_num == "7":
                                color_str = "blue"

                    # study_data = 'st' + str(log.stage) + '-' + color_str
                    study_data['st'] = 'st' + str(log.stage)
                    study_data['st' + str(log.stage)] = 'st' + str(log.stage)
                    study_data['color'] = color_str
                    study_data['color' + str(log.stage)] = color_str
                    # print(study_data)

            else:
                study_data['st'] = '.'
            # print(day_str.strip()[-1])
            # print(dt)
            # member['day' + dt] = str(day_str)
            member.days.append(study_data)
        if member.mname == "전소현":
            print(member.mname)
            print(member.days[0])
            print(member.days[1])
            print(member.days[2])
            print(member.days[3])
            print(member.days[4])
            print(member.days[5])
            print(member.days[6])

    # SELECT "study_info_stepfinishlog"."id", "study_info_stepfinishlog"."username", "study_info_stepfinishlog"."dt_year", "study_info_stepfinishlog"."dt_month", "study_info_stepfinishlog"."dt_day", "study_info_stepfinishlog"."topic_code", "study_info_stepfinishlog"."step_code", "study_info_stepfinishlog"."step_num", "study_info_stepfinishlog"."c_point", "study_info_stepfinishlog"."t_point", "study_info_stepfinishlog"."answer", "study_info_stepfinishlog"."finish_dt", "study_info_stepfinishlog"."stage", "study_info_stepfinishlog"."step" FROM "study_info_stepfinishlog" WHERE ("study_info_stepfinishlog"."dt_day" = 19 AND "study_info_stepfinishlog"."dt_month" = 05 AND "study_info_stepfinishlog"."dt_year" = 22 AND "study_info_stepfinishlog"."username" = 전소현)

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
