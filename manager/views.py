import random
import urllib
import json
from django.core.serializers import serialize
from itertools import groupby
import json
import calendar
from django.core import serializers
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from datetime import date, timedelta, datetime

# Create your views here.
from django.template import RequestContext
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from common_value.models import AppVersion, EtcValue
from library.models import Level, Topic, SpkSent, Theme, Exam, Word, Reading
from manager.models import MemberTopicLog, Plan, PlanDetail, ReportCardMemo
from member_info.models import StudyMember
from study_info.models import StepFinishLog


def comprehension(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('잘못된 접근입니다(topic code)')

    ctrl_user = 0
    if request.GET.get('ctrl_user'):
        ctrl_user = request.GET.get('ctrl_user')

    ctrl_answer = 0
    if request.GET.get('ctrl_answer'):
        ctrl_answer = int(request.GET.get('ctrl_answer'))

    is_member = False
    member_name = ''
    topic_name = ''
    is_user_answer = False
    id = ''
    mcode = ''
    answer_list = []
    if request.GET.get('mcode'):
        mcode = request.GET.get('mcode')
        # 학원생 이름 가져오기
        member = StudyMember.objects.filter(mcode=mcode)
        if member:
            is_member = True
            member = member[0]
            member_name = member.mname

        # 토픽 이름 가져오기
        topic = Topic.objects.filter(topic_code=topic_code)
        if topic:
            topic = topic[0]
            topic_name = topic.topic_name

        id = request.GET.get('id')
        answer_log = StepFinishLog.objects.filter(username=mcode, study_code=id, step_code='P10')
        cnt = 0
        for answer in answer_log:
            cnt += 1
            if answer.answer == 'T':
                answer.answer = 'O'
            if answer.answer == 'F':
                answer.answer = 'X'
            # if cnt < 6:
            answer_list.append(answer.answer)
            # print('answer : ' + str(answer.answer))
            # print('==============' + str(cnt))
        if cnt >= 1:
            is_user_answer = True

    para_list = Reading.objects.filter(topic_code=topic_code)
    for para in para_list:
        para.eng = para.eng.replace(']', '')
        para.eng = para.eng.replace('{', '')
        para.eng = para.eng.replace('[', '')
        para.eng = para.eng.replace('}', '')
        para.eng = para.eng.replace('^', '\n')

    print(len(para_list))
    exam_info = Exam.objects.filter(topic_code=topic_code)
    cnt = 0
    user_answer_len = len(answer_list)
    for row in exam_info:
        row.ask = row.ask.replace('^', '')
        if row.answer == 'T':
            row.answer = 'O'
        if row.answer == 'F':
            row.answer = 'X'

        if user_answer_len > cnt:
            # print('exam.answer : ' + row.answer)
            # print('user.answer : ' + answer_list[cnt])
            row.user = answer_list[cnt]
            # print('===================')
        cnt += 1

    context = {
        'para_len': len(para_list),
        'is_member': is_member,
        'id': id,
        'mcode': mcode,
        'member_name': member_name,
        'topic_name': topic_name,
        'exam_info': exam_info,
        'para_list': para_list,
        'ctrl_answer': str(ctrl_answer),
        'ctrl_user': ctrl_user,
        'is_user_answer': is_user_answer,
        'answer_list': answer_list
    }
    return render(request, 'manager/comprehension.html', context)


def print_page(request):
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

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
        return HttpResponse('잘못된 접근입니다(topic code)')
    exam_info = Exam.objects.filter(topic_code=topic_code)
    context = {'exam_info': exam_info}
    return render(request, 'manager/answer.html', context)


def interpretation(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('잘못된 접근입니다 (topic code)')

    # 영어 / 한글 표시
    reading_type = 'both'  # eng, kor, both(eng+kor)
    if request.GET.get('type'):
        reading_type = request.GET.get('type')

    is_name = False
    user_name = ''
    if request.GET.get('user_name'):
        user_name = request.GET.get('user_name')
        if user_name != '':
            is_name = True

    # 순차적 / 랜덤 표시
    is_random = 'normal'
    if request.GET.get('random'):
        is_random = request.GET.get('random')

    topic_info = Topic.objects.get(topic_code=topic_code)
    theme_info = Theme.objects.get(theme_code=topic_info.theme_code)
    level_info = Level.objects.get(level_code=theme_info.level_code)

    if is_random == 'normal':
        sentence_list = Reading.objects.filter(topic_code=topic_code)
    else:
        sentence_list = Reading.objects.filter(topic_code=topic_code).order_by('?')

    for row in sentence_list:
        row.eng = row.eng.replace('{', '')
        row.eng = row.eng.replace('}', '')
        row.eng = row.eng.replace('[', '')
        row.eng = row.eng.replace(']', '')
        row.eng = row.eng.replace('^', '\n')

        row.kor = row.kor.replace('{', '')
        row.kor = row.kor.replace('}', '')
        row.kor = row.kor.replace('[', '')
        row.kor = row.kor.replace(']', '')
        row.kor = row.kor.replace('^', '\n')

    context = {
        'level_info': level_info,
        'theme_info': theme_info,
        'topic_info': topic_info,
        'reading_type': reading_type,  # eng, kor, eng+kor
        'random': is_random,
        'sentence_list': sentence_list,
        'is_name': is_name,
        'user_name': user_name,
    }
    return render(request, 'manager/interpretation.html', context)


def reportcard(request, mcode=''):
    if mcode == '':
        return HttpResponse('잘못된 접근입니다 (topic code)')

    # 날짜 리스트 생성
    year_list, month_list, day_list = generate_date_lists()

    # 날짜 필터 설정
    sy, ey, sm, sd, em, ed = get_date_filters(request)  # 'sy'와 'ey' 추가

    user_name = ''
    study_start_day = ''
    study_end_day = ''
    level_name = ''
    member = StudyMember.objects.filter(mcode=mcode)
    if member:
        member = member[0]
        user_name = member.mname
        level_name = member.level_code

    if sm and em and sd != '0' and ed != '0':
        print('ok, get data!')

        start_date = datetime(int(sy), int(sm), int(sd), 0, 0, 0)  # 'sy' 추가
        end_date = datetime(int(ey), int(em), int(ed), 23, 59, 59)  # 'ey' 추가
        topic_list = MemberTopicLog.objects.filter(username=mcode, start_dt__gte=start_date,
                                                   end_dt__lt=end_date).order_by('-id')
        first_topic = topic_list.order_by('id').first()
        last_topic = topic_list.order_by('-id').first()
        if first_topic:
            study_start_day = first_topic.start_dt
        if last_topic:
            study_end_day = last_topic.end_dt
    else:
        topic_list = MemberTopicLog.objects.filter(username=mcode).order_by('-id')
        first_topic = topic_list.order_by('id').first()
        last_topic = topic_list.order_by('-id').first()
        if first_topic:
            study_start_day = first_topic.start_dt
        if last_topic:
            study_end_day = last_topic.end_dt

    memo_list = ReportCardMemo.objects.filter(visible=1).order_by('seq')
    for memo in memo_list:
        memo.memo = memo.memo.replace('ㅇㅇ', user_name)

    context = {
        'memo_list': memo_list,
        'year_list': year_list,  # 연도 리스트 추가
        'month_list': month_list,
        'day_list': day_list,
        'sy': sy,  # 시작 연도
        'ey': ey,  # 종료 연도 추가
        'sm': sm,
        'sd': sd,
        'em': em,
        'ed': ed,

        'user_name': user_name,
        'level_name': level_name,
        'topic_list': topic_list,
        'study_start_day': study_start_day,
        'study_end_day': study_end_day,
    }
    return render(request, 'manager/reportcard.html', context)



def reportSelect(request):
    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    # update_member_list(request, aid)
    call(request)

    is_select_level = False
    select_level_name = ''
    select_plan_name = ''
    user_name = ''
    level_list = []
    plan_list = []
    desc = '0'
    switch_desc = '1'
    query_desc = ''

    order_by = 'mname'
    if request.GET.get('desc'):
        desc = request.GET.get('desc')
        if desc == '1':
            switch_desc = '0'
            query_desc = '-'
        else:
            desc = '0'
            switch_desc = '1'
            query_desc = ''

    member_list = StudyMember.objects.filter(acode=aid, list_enable=1).order_by(query_desc + order_by)
    total_cnt = len(member_list)
    for member in member_list:
        if member.level_code is None:
            member.level_code = Level.objects.get(level_code=200)

        level_list = Level.objects.filter(show_level__gte=1).order_by('index_order')
        plan_list = Plan.objects.all().order_by('seq')

    else:
        user_id = ''

    context = {
        'desc': desc,
        'switch_desc': switch_desc,
        'isSelectLevel': is_select_level,
        'select_level_name': select_level_name,
        'select_plan_name': select_plan_name,
        'member_list': member_list,
        'level_list': level_list,
        'plan_list': plan_list,
        'user_name': user_name,
        'user_id': user_id,
        'total_cnt': total_cnt
    }
    return render(request, 'manager/report_select.html', context)


def reportall(request):
    aid = get_aid(request)

    # 체크 리스트 처리
    handle_check_list(request, aid)

    # 날짜 리스트 생성
    year_list, month_list, day_list = generate_date_lists()

    # 날짜 필터 설정
    sy, ey, sm, sd, em, ed = get_date_filters(request)  # 'ey' 추가

    # 보고서 리스트 생성
    report_list = create_report_list(aid, sy, sm, sd, ey, em, ed)  # 매개변수 순서 및 'ey' 추가

    # 메모 리스트
    memo_list = ReportCardMemo.objects.filter(visible=1).order_by('seq')

    context = {
        'memo_list': memo_list,
        'year_list': year_list,  # 연도 리스트 추가
        'month_list': month_list,
        'day_list': day_list,
        'sy': sy,  # 시작 연도
        'ey': ey,  # 종료 연도 추가
        'sm': sm,
        'sd': sd,
        'em': em,
        'ed': ed,
        'report_list': report_list,
    }
    return render(request, 'manager/reportcardall.html', context)


def handle_check_list(request, aid):
    if request.GET.getlist('check_list'):
        StudyMember.objects.filter(acode=aid).update(is_check=0)
        check_mem_list = request.GET.getlist('check_list')
        StudyMember.objects.filter(acode=aid, mcode__in=check_mem_list).update(is_check=1)

def generate_date_lists():
    current_year = datetime.now().year
    year_list = [str(year) for year in range(current_year - 5, current_year + 1)]  # 예: 현재 연도에서 5년 전부터 현재 연도까지
    month_list = [str(x) for x in range(1, 13)]
    day_list = [str(x) for x in range(1, 32)]
    return year_list, month_list, day_list


def get_date_filters(request):
    sy = request.GET.get('sy', str(datetime.now().year))  # 시작 연도
    ey = request.GET.get('ey', str(datetime.now().year))  # 종료 연도
    sm = request.GET.get('sm', '')
    sd = request.GET.get('sd', '0')
    em = request.GET.get('em', '0')
    ed = request.GET.get('ed', '0')
    return sy, ey, sm, sd, em, ed


def create_report_list(aid, sy, sm, sd, ey, em, ed):
    report_list = []
    member_list = StudyMember.objects.filter(acode=aid, list_enable=1, is_check=1).order_by('mname')
    for member in member_list:
        report = create_report(member, sy, sm, sd, ey, em, ed)
        report_list.append(report)
    return report_list


def create_report(member, sy, sm, sd, ey, em, ed):
    report = {'user_name': member.mname, 'level_name': member.level_code}
    if sm and em and sd != '0' and ed != '0':
        start_date = datetime(int(sy), int(sm), int(sd), 0, 0, 0)
        end_date = datetime(int(ey), int(em), int(ed), 23, 59, 59)
        report['topic_list'] = get_topics(member.mcode, start_date, end_date)
    else:
        report['topic_list'] = MemberTopicLog.objects.filter(username=member.mcode).order_by('-id')

    set_study_period(report)
    return report


def get_topics(mcode, start_date, end_date):
    return MemberTopicLog.objects.filter(
        username=mcode, start_dt__gte=start_date, end_dt__lt=end_date
    ).order_by('-id')


def set_study_period(report):
    if report['topic_list']:
        report['study_start_day'] = report['topic_list'].first().start_dt
        report['study_end_day'] = report['topic_list'].last().end_dt


def get_aid(request):
    if 'agency' in request.session:
        aid = request.session['agency']
        return aid
    else:
        return 'bad_way'


def agency(request, agency_id=''):
    """
        올리 관리자 페이지에서는 로그인 페이지가 없다. 포겟미낫 관리자 페이지 우상단에서
        [올리] 를 클릭하면 이쪽으로 오도록 회의에서 결정하였다.
        따라서 그러한 루트로 아래 agency에 접근하면 세션을 등록하고, 그것으로 아이디처럼 사용하도록 한다. """
    if agency_id == '':
        return HttpResponse('잘못된 접근입니다')
    else:
        request.session['agency'] = agency_id
        return HttpResponseRedirect(reverse('manager:info'))


def update_member_list(request, agency_id):
    """
        웹전산 API에서 원장님 아이디에 해당하는 학생들을 불러온다.
        불러온 리스트가 DB에 없다면 추가해준다.
        페이지를 호출할때마다 매번 추가할 순 없으니 세션을 등록해주어 반복 실행을 막는다. """

    # 세션이 등록 되어 있다면 나가기
    if 'sync_member3' in request.session:
        print('already sync!')
        pass
    else:
        print('going down!')
    # 웹전산에서 정보 가져오기 -- JSON
    # http://www.tongclass.co.kr/Class/api_member.aspx?ac=gyeong8890
    # gyeong8890
    url = "http://www.tongclass.co.kr/Class/api_member.aspx?ac=" + agency_id
    oper_url = urllib.request.urlopen(url)
    if oper_url.getcode() == 200:
        data = oper_url.read().decode(oper_url.headers.get_content_charset())
        json_data = json.loads(data)
        for row in json_data:
            row_id = row['Id']
            row_id = str(row_id).lower()
            row_name = row['Mn']
            # print(row_id + '/' + row_name)
            # 회원이 없다면 등록시키기.
            study_member = StudyMember.objects.filter(mcode=row_id)
            if study_member:
                study_member = study_member[0]
                if study_member.acode is None:
                    study_member.acode = agency_id
                    study_member.save()
            else:
                study_member = StudyMember(mcode=row_id, mname=row_name, acode=agency_id,
                                           plan_code=Plan.objects.get(plan_code=2))
                study_member.save()

    # 웹전산에서 학원 이름 가져오기 -- JSON
    url = "http://www.tongclass.co.kr/Class/api_agency_name.aspx?ac=" + agency_id
    oper_url = urllib.request.urlopen(url)
    if oper_url.getcode() == 200:
        data = oper_url.read().decode(oper_url.headers.get_content_charset())
        json_data = json.loads(data)
        aname = json_data['Mn']
        print('a name : ' + aname)
        request.session['aname'] = aname

    # 세션 등록
    request.session['sync_member3'] = 'ok'


def btns(request, code=''):
    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    result = ''
    # 만약에 아이디가 etong이 아니라면 접근 금지.
    if aid != 'etong': return HttpResponse(
        '<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    if code == 'za1880aab33231sdaeealekea23z':
        start_dt = date.today()
        day = start_dt - timedelta(0)
        yy = day.strftime('%y')
        mm = day.strftime('%m')
        dd = day.strftime('%d')
        m = int(mm)
        if m > 3:
            # print('m : ' + str(m))
            m = m - 2
            # print('m : ' + str(m))
            mm = str(m)
            if m < 10:
                mm = '0' + mm
            # print('mm : ' + mm)
            log_list = StepFinishLog.objects.filter(dt_year__lte=yy, dt_month__lte=mm)
            list_len = len(log_list)
            # print('len : ' + str(list_len))
            if list_len > 0:
                log_list.delete()
                result = 'work'
            else:
                result = 'not work, is zero'
            return HttpResponse(code + '/' + yy + '/' + mm + '/' + str(list_len) + '/' + result)

    code = 'code zero'
    return HttpResponse(code)


def info(request, user_id=''):
    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    # update_member_list(request, aid)
    call(request)

    is_select_level = False
    select_level_name = ''
    select_plan_name = ''
    user_name = ''
    level_list = []
    plan_list = []
    member_topic_log = []
    desc = '0'
    switch_desc = '1'
    query_desc = ''

    order_by = 'mname'
    if request.GET.get('desc'):
        desc = request.GET.get('desc')
        if desc == '1':
            switch_desc = '0'
            query_desc = '-'
        else:
            desc = '0'
            switch_desc = '1'
            query_desc = ''

    member_list = StudyMember.objects.filter(acode=aid, list_enable=1).order_by(query_desc + order_by)
    for member in member_list:
        if member.level_code is None:
            member.level_code = Level.objects.get(level_code=200)

    if user_id != '':
        user = StudyMember.objects.filter(mcode=user_id)
        if user:
            user = user[0]
            is_select_level = True

            # 1. 레벨/플랜 변경 처리
            # ----------------------
            # - 레벨 변경 (btn_level)
            # - 플랜 변경 (btn_plan)
            if request.GET.get('mem_level') or request.GET.get('mem_plan'):
                mem_level = request.GET.get('mem_level')
                mem_plan = request.GET.get('mem_plan')

                # 혹시 "플랜 변경" 버튼(btn_plan)을 눌렀다면 → 진행 중 학습 강제 종료 로직
                if 'btn_plan' in request.GET:
                    # 진행 중(end_dt == None)인 가장 최근 MemberTopicLog 찾기
                    latest_log = MemberTopicLog.objects.filter(
                        username=user_id,
                        end_dt__isnull=True
                    ).order_by('-id').first()

                    if latest_log:
                        # 종료 처리
                        latest_log.end_dt = datetime.now()
                        latest_log.save()

                        # StepFinishLog 기록 (기존 로직 준용)
                        today = date.today()
                        year = today.strftime('%y')
                        month = today.strftime('%m')
                        day = today.strftime('%d')
                        StepFinishLog.objects.create(
                            username=user_id,
                            dt_year=year,
                            dt_month=month,
                            dt_day=day,
                            topic_code='C'
                            # 나머지는 None
                        )

                        # user.current_study도 초기화
                        user.current_study = 0
                        user.save()

                # 이제 레벨/플랜 실제 변경
                user.level_code = Level.objects.get(level_code=mem_level)
                user.plan_code = Plan.objects.get(plan_code=mem_plan)
                user.save()
                return HttpResponseRedirect(reverse('manager:info', args=(user_id,)))


            # 토픽 종료 또는 토픽 리셋 실행.
            if request.GET.get('process'):
                process = request.GET.get('process')
                process_id = request.GET.get('process_id')
                log = MemberTopicLog.objects.get(id=process_id)
                if log:
                    today = date.today()
                    year = today.strftime('%y')
                    month = today.strftime('%m')
                    day = today.strftime('%d')

                    user = StudyMember.objects.filter(mcode=user_id)  # 종료일 경우 현재 학습을 0, 리셋을 경우 상황에 따라 0
                    user = user[0]
                    if process == 'closed':
                        log.end_dt = datetime.now()
                        save_topic = StepFinishLog(username=user_id, dt_year=year, dt_month=month,
                                                   dt_day=day, topic_code='C', step_code=None,
                                                   step_num=None, c_point=None, t_point=None,
                                                   answer=None, stage=None, step=None, plan_type=None,
                                                   study_code=None)
                        save_topic.save()
                        user.current_study = 0
                        log.save()
                        user.save()

                    elif process == 'reset':
                        if log.id == user.current_study:
                            user.current_study = 0
                            user.save()
                        log.delete()

                    return HttpResponseRedirect(reverse('manager:info', args=(user_id,)))

        level_list = Level.objects.filter(show_level__gte=1).order_by('index_order')
        select_level_name = str(user.level_code)
        select_plan_name = str(user.plan_code)
        plan_list = Plan.objects.all().order_by('seq')
        user_name = user.mname
        member_topic_log = MemberTopicLog.objects.filter(username=user_id).order_by('-id')

    else:
        user_id = ''

    context = {
        'desc': desc,
        'switch_desc': switch_desc,
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


class WeekListView(ListView):
    model = StepFinishLog
    context_object_name = 'week_list'
    template_name = 'manager/week_list_dev.html'
    ordering = '-id'
    paginate_by = 20


def week_up(request, prev_dt=0):
    ## week 와 week_up 체인지.
    # DB에서 이 메뉴를 사용할 것인지 체크를 해본다.
    enable_data = EtcValue.objects.filter(etc_name='WEEK_MENU_ENABLE')
    if enable_data:
        enable_data = enable_data[0];
        # print(enable_data.etc_value)
        if enable_data.etc_value != '1':
            return HttpResponseRedirect(reverse('manager:info'))

    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    # update_member_list(request, aid)
    call(request)

    start_dt = date.today()

    # 시작일 기준 전날 6일 날짜 가져오기 - 테이블 상단용
    days = []
    loop = 6
    for n in range(7):
        seek = loop - n
        day = start_dt - timedelta(seek + prev_dt)
        day_str = day.strftime('%m.%d') + get_day(day.weekday())
        # print(day_str.strip()[-1])
        days.append(day_str)

    desc = ''
    order = 'mname'

    switch_desc = '1'
    query_desc = ''

    order_by = 'mname'
    if request.GET.get('desc'):
        desc = request.GET.get('desc')
        if desc == '1':
            switch_desc = '0'
            query_desc = '-'
        else:
            desc = '0'
            switch_desc = '1'
            query_desc = ''

    # 모든 학생에 대해 7일간 학습 데이터 가져오기
    member_list = StudyMember.objects.filter(acode=aid, list_enable=1).order_by(query_desc + order)
    # 01 모든 학생을 가져온다.
    for member in member_list:
        member.days = []
        loop = 6

        # 02 한 학생당 지정된(seek) 날짜로부터 지난 7일간의 날짜를 가져온다.
        for dt in range(7):
            seek = loop - dt
            day = start_dt - timedelta(seek + prev_dt)
            day_str = day.strftime('%m.%d') + get_day(day.weekday())
            yy = day.strftime('%y')
            mm = day.strftime('%m')
            dd = day.strftime('%d')
            append_data_list = []

            # 03 날짜당 학생의 데이터를 추출해본다.

            log_list = StepFinishLog.objects.filter(username=member.mcode, dt_year=yy, dt_month=mm, dt_day=dd).order_by(
                '-id')
            if log_list:
                log_data = {}
                log_data['yy'] = yy
                log_data['mm'] = mm
                log_data['dd'] = dd
                prev_log = {}
                prev_log['text'] = 'st'
                prev_log['color'] = 'black'
                prev_log['stage'] = 0
                prev_log['step'] = 0
                for log in log_list:
                    # print(' --' + member.mcode + '/' + str(log.stage) + '/' + str(log.step))
                    log_data = {}
                    log_data['yy'] = yy
                    log_data['mm'] = mm
                    log_data['dd'] = dd
                    log_data['stage'] = log.stage
                    log_data['step'] = log.step
                    log_data['text'] = 'st' + str(log.stage)
                    log_data['color'] = 'colorGray'
                    if log.plan_type == 2:
                        # ////////// 자 유 학 습 /////////////////////////////////////////////
                        if log.step == 7 or log.step_num != '0':
                            # log.step == 7 은 정오답 체크 / log.step_num != '0'은 문제 풀이(1~6)
                            log_data['text'] = 'Q'
                            log_data['color'] = 'colorForestGreen'
                            if prev_log['text'] != 'Q':
                                append_data_list.insert(0, log_data)
                                prev_log['text'] = 'Q'
                        else:
                            # 그 외 스텝일 때
                            log_data['text'] = str(log.step)
                            log_data['color'] = 'colorGreen'
                            append_data_list.insert(0, log_data)
                    elif log.topic_code == 'C':
                        # //////////  종 료 /////////////////////////////////////////////
                        log_data['text'] = 'C'
                        log_data['color'] = 'colorIndigo'
                        append_data_list.insert(0, log_data)
                    elif log.topic_code == 'R':
                        # ////////// 리 셋 /////////////////////////////////////////////
                        log_data['text'] = 'R'
                        log_data['color'] = 'colorRed'
                        append_data_list.insert(0, log_data)
                    else:
                        # ////////// 완 전 학 습 ////////////////////////////////////////////
                        if log.finish_today:
                            log_data['color'] = 'colorBlue'

                        if prev_log['stage'] != log_data['stage']:
                            append_data_list.insert(0, log_data)

                    prev_log['stage'] = log_data['stage']

            else:
                log_data = {}
                log_data['yy'] = yy
                log_data['mm'] = mm
                log_data['dd'] = dd
                log_data['color'] = ''
                log_data['text'] = '.'
                append_data_list.append(log_data)

            # member마다 7일간 데이터 저장.
            member.days.append(append_data_list)

    prev_week = prev_dt + 7
    next_week = prev_dt - 7
    if next_week < 0:
        next_week = 0
    context = {
        'switch_desc': switch_desc,
        'prev_week': prev_week,
        'next_week': next_week,
        'arg': prev_dt,
        'start_dt': start_dt,
        'days': days,
        'member_list': member_list,
    }
    return render(request, 'manager/week.html', context)


def week(request, prev_dt=0):
    # DB에서 이 메뉴를 사용할 것인지 체크를 해본다.
    enable_data = EtcValue.objects.filter(etc_name='WEEK_MENU_ENABLE')
    if enable_data:
        enable_data = enable_data[0];
        # print(enable_data.etc_value)
        if enable_data.etc_value != '1':
            return HttpResponseRedirect(reverse('manager:info'))

    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    # update_member_list(request, aid)
    call(request)

    start_dt = date.today()
    end_dt = start_dt - timedelta(days=6 + prev_dt)  # 주의 시작 날짜 계산

    # 시작일 기준 전날 6일 날짜 가져오기 - 테이블 상단용
    days = []
    dates = []
    loop = 6
    redirect_needed = False
    for n in range(7):
        seek = loop - n
        day = start_dt - timedelta(seek + prev_dt)
        dates.append(day)
        day_str = day.strftime('%m.%d') + get_day(day.weekday())
        days.append(day_str)

    desc = ''
    order = 'mname'

    switch_desc = '1'
    query_desc = ''

    order_by = 'mname'
    if request.GET.get('desc'):
        desc = request.GET.get('desc')
        if desc == '1':
            switch_desc = '0'
            query_desc = '-'
        else:
            desc = '0'
            switch_desc = '1'
            query_desc = ''

    # 모든 학생에 대해 7일간 학습 데이터 가져오기
    member_list = StudyMember.objects.filter(acode=aid, list_enable=1).order_by(query_desc + order)

    # 모든 학생의 mcode를 리스트로 추출
    mcode_list = member_list.values_list('mcode', flat=True)

    # Generate a list of date tuples (year, month, day) for the date range
    date_tuples = [(d.strftime('%y'), d.strftime('%m'), d.strftime('%d')) for d in
                   [start_dt - timedelta(days=x) for x in range(prev_dt, prev_dt + 7)]]

    # 해당 기간 동안의 모든 학습 로그 한 번에 가져오기
    logs = StepFinishLog.objects.filter(
        username__in=mcode_list,
        dt_year__in=[dt[0] for dt in date_tuples],
        dt_month__in=[dt[1] for dt in date_tuples],
        dt_day__in=[dt[2] for dt in date_tuples]
    ).order_by('-id')

    # 로그를 사용자와 날짜별로 정리
    logs_by_user_and_date = {}
    for log in logs:
        key = (log.username, log.dt_year, log.dt_month, log.dt_day)
        if key not in logs_by_user_and_date:
            logs_by_user_and_date[key] = []
        logs_by_user_and_date[key].append(log)

    # 01 모든 학생을 가져온다.
    for member in member_list:
        member.days = []
        seen_stages = set()  # Initialize seen stages

        # 02 한 학생당 지정된(seek) 날짜로부터 지난 7일간의 날짜를 가져온다.
        for dt in range(7):
            seek = loop - dt
            day = start_dt - timedelta(seek + prev_dt)
            day_str = day.strftime('%m.%d') + get_day(day.weekday())
            yy = day.strftime('%y')
            mm = day.strftime('%m')
            dd = day.strftime('%d')
            append_data_list = []
            seen_stages.clear()  # Reset seen stages for the new day
            prev_log = {'text': 'st', 'color': 'black', 'stage': 0, 'step': 0}  # Reset prev_log for the new day

            # 로그를 사용자와 날짜별로 정리된 데이터에서 현재 날짜의 로그를 가져옴
            key = (member.mcode, yy, mm, dd)
            if key in logs_by_user_and_date:
                for log in logs_by_user_and_date[key]:
                    # log 데이터를 처리하는 로직
                    log_data = {'yy': yy, 'mm': mm, 'dd': dd, 'stage': log.stage, 'step': log.step,
                                'text': 'st' + str(log.stage), 'color': 'colorGray'}

                    if log.plan_type == 2:
                        # ////////// 자 유 학 습 /////////////////////////////////////////////
                        if log.step == 7 or log.step_num != '0':
                            # log.step == 7 은 정오답 체크 / log.step_num != '0'은 문제 풀이(1~6)
                            log_data['text'] = 'Q'
                            log_data['color'] = 'colorForestGreen'
                            if prev_log['text'] != 'Q':
                                if log_data['stage'] not in seen_stages:
                                    append_data_list.insert(0, log_data)
                                    prev_log['text'] = 'Q'
                                    seen_stages.add(log_data['stage'])
                        else:
                            # ////// 그 외 스텝일 때
                            log_data['text'] = str(log.step)
                            log_data['color'] = 'colorGreen'
                            append_data_list.insert(0, log_data)
                    elif log.topic_code == 'C':
                        # //////////  종 료 /////////////////////////////////////////////
                        log_data['text'] = 'C'
                        log_data['color'] = 'colorIndigo'
                        if log_data['stage'] not in seen_stages:
                            append_data_list.insert(0, log_data)
                            seen_stages.add(log_data['stage'])
                    elif log.topic_code == 'R':
                        # ////////// 리 셋 /////////////////////////////////////////////
                        log_data['text'] = 'R'
                        log_data['color'] = 'colorRed'
                        if log_data['stage'] not in seen_stages:
                            append_data_list.insert(0, log_data)
                            seen_stages.add(log_data['stage'])
                    else:
                        # ////////// 완 전 학 습 ////////////////////////////////////////////
                        log_data['text'] = 'st' + str(log.stage)
                        log_data['color'] = 'colorGray' if not log.finish_today else 'colorBlue'

                    # 데이터를 추가하기 전에 조건들을 체크
                    if log_data['stage'] not in seen_stages:
                        append_data_list.insert(0, log_data)
                        seen_stages.add(log_data['stage'])

                    prev_log['stage'] = log.stage
                    prev_log['color'] = log_data['color']
            else:
                # 로그 데이터가 없고, 이전 로그의 색상이 'colorBlue'인 경우 (이전 날에 학습이 완료된 경우)
                if prev_log['color'] == 'colorBlue':
                    # 같은 stage의 'colorBlue' 데이터를 기본 데이터로 설정
                    log_data = {'yy': yy, 'mm': mm, 'dd': dd, 'color': 'colorBlue',
                                'text': 'st' + str(prev_log['stage'])}
                else:
                    # 그렇지 않으면, '.' 데이터 설정
                    log_data = {'yy': yy, 'mm': mm, 'dd': dd, 'color': '', 'text': '.'}
                append_data_list.append(log_data)

            # member마다 7일간 데이터 저장.
            member.days.append(append_data_list)

    # 나머지 코드 ...
    prev_week = prev_dt + 7
    next_week = prev_dt - 7
    if next_week < 0:
        next_week = 0
    context = {
        'switch_desc': switch_desc,
        'prev_week': prev_week,
        'next_week': next_week,
        'arg': prev_dt,
        'start_dt': start_dt,
        'days': days,
        'member_list': member_list,
    }
    return render(request, 'manager/week.html', context)


def get_week_dates(start_dt):
    return [(start_dt - timedelta(days=i)).strftime('%m.%d') + get_day((start_dt - timedelta(days=i)).weekday()) for i
            in range(6, -1, -1)]


def get_week_logs(member_list, start_dt, end_dt):
    week_logs = StepFinishLog.objects.filter(
        username__in=member_list.values_list('mcode', flat=True),
        dt_year=start_dt.strftime('%y'),
        dt_month=start_dt.strftime('%m'),
        dt_day__range=[start_dt.strftime('%d'), end_dt.strftime('%d')]
    ).order_by('-id')
    return week_logs


def organize_logs_by_member_date(week_logs):
    logs_by_member_date = {
        (log.username, log.dt_year, log.dt_month, log.dt_day): log for log in week_logs
    }
    return logs_by_member_date





def day(request):
    mname = request.GET.get('mname')
    mcode = request.GET.get('mcode')
    yy = request.GET.get('yy')
    mm = request.GET.get('mm')
    dd = request.GET.get('dd')

    log_list = StepFinishLog.objects.filter(username=mcode, dt_year=yy, dt_month=mm, dt_day=dd).order_by(
        '-id')
    if log_list:
        append_data_list = []
        log_data = {}
        prev_log = {}
        prev_log['text'] = 'st'
        prev_log['color'] = 'black'
        prev_log['stage'] = 0
        prev_log['step'] = 0
        for log in log_list:
            # print(' --' + member.mcode + '/' + str(log.stage) + '/' + str(log.step))
            log_data = {}
            log_data['stage'] = log.stage
            log_data['step'] = log.step
            log_data['text'] = 'st' + str(log.stage)
            log_data['color'] = 'colorGray'
            log_data['topic'] = ''
            if log.plan_type == 2:
                topic = Topic.objects.filter(topic_code=log.topic_code)
                theme = Theme.objects.filter(theme_code=topic[0].theme_code)
                level = Level.objects.filter(level_code=theme[0].level_code)
                log_data['level'] = level[0].level_name
                log_data['theme'] = theme[0].theme_name
                log_data['topic'] = topic[0].topic_name
                # ////////// 자 유 학 습 /////////////////////////////////////////////
                if log.step == 7 or log.step_num != '0':
                    # log.step == 7 은 정오답 체크 / log.step_num != '0'은 문제 풀이(1~6)
                    log_data['text'] = 'Q'
                    log_data['color'] = 'colorForestGreen'
                    if prev_log['text'] != 'Q':
                        append_data_list.insert(0, log_data)
                        prev_log['text'] = 'Q'
                else:
                    # 그 외 스텝일 때
                    log_data['text'] = str(log.step)
                    log_data['color'] = 'colorGreen'
                    append_data_list.insert(0, log_data)
            elif log.topic_code == 'C':
                # //////////  종 료 /////////////////////////////////////////////
                log_data['text'] = 'C'
                log_data['color'] = 'colorIndigo'
                append_data_list.insert(0, log_data)
            elif log.topic_code == 'R':
                # ////////// 리 셋 /////////////////////////////////////////////
                log_data['text'] = 'R'
                log_data['color'] = 'colorRed'
                append_data_list.insert(0, log_data)
            else:
                topic = Topic.objects.filter(topic_code=log.topic_code)
                theme = Theme.objects.filter(theme_code=topic[0].theme_code)
                level = Level.objects.filter(level_code=theme[0].level_code)
                log_data['level'] = level[0].level_name
                log_data['theme'] = theme[0].theme_name
                log_data['topic'] = topic[0].topic_name
                # ////////// 완 전 학 습 /////////////////////////////////////////////
                if log.finish_today:
                    log_data['color'] = 'colorBlue'

                if prev_log['stage'] != log_data['stage']:
                    append_data_list.insert(0, log_data)

            prev_log['stage'] = log_data['stage']

    context = {
        'mname': mname,
        'mcode': mcode,
        'yy': yy,
        'mm': mm,
        'dd': dd,
        'row_list': append_data_list,
    }
    return render(request, 'manager/day.html', context)


def downapp(request):
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    ver = AppVersion.objects.filter().order_by('-id')
    ver = ver[0]
    url = ver.download_url
    runtime_win = 'http://www.vocafmn.co.kr/Upload/AttachFile/ar_update/AdobeAIR.exe'
    runtime_mac = 'https://airsdk.harman.com/assets/downloads/AdobeAIR.dmg'
    context = {
        'url': url,
        'win': runtime_win,
        'mac': runtime_mac
    }
    return render(request, 'manager/downapp.html', context)


def get_day(num):
    switcher = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
    return switcher.get(num, "Please enter number between 1-7")


def plan_view(request):
    return render(request, 'manager/plan_view.html')


def plan_info(request):
    plan_list = Plan.objects.all()
    prev_stage = 0
    all_plan = []
    for plan in plan_list:
        new_plan = {}
        new_plan['name'] = plan.plan_name
        stage_info = {}
        stage_list = []
        new_plan['stage_info'] = stage_info
        stage_info['stage_list'] = stage_list

        # print('<' + plan.plan_name + '>')
        detail_list = PlanDetail.objects.filter(plan_code=plan.plan_code)
        for detail in detail_list:
            if prev_stage != detail.stage:
                # print('=stage ' + str(detail.stage) + '=')
                stage_list.append('=stage ' + str(detail.stage) + '=')
                step_list = []
                stage_info['step_list'] = step_list
            # print('--step' + str(detail.seq) + ' : ' + str(detail.step))
            step_list.append(str(detail.seq) + ' : ' + str(detail.step))
            prev_stage = detail.stage
        # print('____')

        all_plan.append(new_plan)
    context = {
        'all_plan': all_plan
    }
    return render(request, 'manager/plan_list.html', context)


def dashboard(request):
    return render(request, 'manager/dashboard.html')


def basic_table(request):
    return render(request, 'manager/basic-table.html')


def profile(request):
    return render(request, 'manager/profile.html')


def call(request):
    aid = get_aid(request)

    # 모든 학생을 리스트 비활성화 시킨다.
    study_member = StudyMember.objects.filter(acode=aid)
    if study_member:
        for member in study_member:
            member.list_enable = 0
            member.save()

    # 가져온 리스트에서 일치하는 학생들은 리스트를 활성화 시킨다.
    url = "http://www.tongclass.co.kr/Class/api_member.aspx?ac=" + aid
    oper_url = urllib.request.urlopen(url)
    if oper_url.getcode() == 200:
        data = oper_url.read().decode(oper_url.headers.get_content_charset())
        json_data = json.loads(data)
        for row in json_data:
            row_id = row['Id']
            row_id = str(row_id).lower()
            row_name = row['Mn']
            # print(row_id + '/' + row_name)
            # 리스트를 활성화, 학원이 비어 있다면 등록
            study_member = StudyMember.objects.filter(mcode=row_id)
            if study_member:
                study_member = study_member[0]
                if study_member.acode is None:
                    study_member.acode = aid
                study_member.list_enable = 1
                study_member.save()
            else:
                # 가져온 리스트에서 없는 학생들은 추가를 해주며 활성화 시킨다.
                study_member = StudyMember(mcode=row_id, mname=row_name, acode=aid,
                                           plan_code=Plan.objects.get(plan_code=2), list_enable=1)
                study_member.save()
    # ok

    # 웹전산에서 학원 이름 가져오기 -- JSON
    url = "http://www.tongclass.co.kr/Class/api_agency_name.aspx?ac=" + aid
    oper_url = urllib.request.urlopen(url)
    if oper_url.getcode() == 200:
        data = oper_url.read().decode(oper_url.headers.get_content_charset())
        json_data = json.loads(data)
        aname = json_data['Mn']
        # print('a name : ' + aname)
        request.session['aname'] = aname

    return HttpResponse(aid)


def test(request):
    context = {
        'user': 'aa',
    }
    return render(request, 'manager/test.html', context)


def test2(request):
    name = request.GET.get('name')
    # request.GET.get('mname')
    age = request.GET.get('age')

    template = get_template('manager/test2.html')

    context = {
        'name': name,
        'age': age,
    }
    return render(request, 'manager/test2.html', context)
