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

from common_value.models import AppVersion
from library.models import Level, Topic, SpkSent, Theme, Exam, Word
from manager.models import MemberTopicLog, Plan, PlanDetail
from member_info.models import StudyMember
from study_info.models import StepFinishLog


def comprehension(request, topic_code=''):
    if topic_code == '':
        return HttpResponse('잘못된 접근입니다(topic code)')

    exam_info = Exam.objects.filter(topic_code=topic_code)
    context = {'exam_info': exam_info}
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

    # 순차적 / 랜덤 표시
    is_random = 'normal'
    if request.GET.get('random'):
        is_random = request.GET.get('random')

    topic_info = Topic.objects.get(topic_code=topic_code)
    theme_info = Theme.objects.get(theme_code=topic_info.theme_code)
    level_info = Level.objects.get(level_code=theme_info.level_code)

    if is_random == 'normal':
        sentence_list = SpkSent.objects.filter(topic_code=topic_code)
    else:
        sentence_list = SpkSent.objects.filter(topic_code=topic_code).order_by('?')

    context = {
        'level_info': level_info,
        'theme_info': theme_info,
        'topic_info': topic_info,
        'reading_type': reading_type,  # eng, kor, eng+kor
        'random': is_random,
        'sentence_list': sentence_list,
    }
    return render(request, 'manager/interpretation.html', context)


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
                if study_member[0].acode is None:
                    study_member[0].acode = agency_id
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


def info(request, user_id=''):
    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    update_member_list(request, aid)

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
            return HttpResponseRedirect(reverse('manager:info', args=(user_id,)))

        # 토픽 종료 또는 토픽 리셋 실행.
        if request.GET.get('process'):
            process = request.GET.get('process')
            process_id = request.GET.get('process_id')
            log = MemberTopicLog.objects.filter(id=process_id)
            if log:
                log = log[0]
                today = date.today()
                year = today.strftime('%y')
                month = today.strftime('%m')
                day = today.strftime('%d')

                user = StudyMember.objects.get(mcode=user_id) # 종료일 경우 현재 학습을 0, 리셋을 경우 상황에 따라 0

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
                    user.current_study = 0
                    user.save()

                elif process == 'reset':
                    log.start_dt = datetime.now()
                    log.end_dt = None
                    log.stage = 1
                    log.step = 1
                    user.current_study = log.id
                    user.save()
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
    paginate_by = 20


def week(request, prev_dt=0):
    # 세션을 확인하여 포겟미낫을 통해 등록된 세션이 없다면 넘어가지 못하게 처리 (agency 함수 참고)
    aid = get_aid(request)
    if aid == 'bad_way': return HttpResponse('<br><br><center>잘못된 접근입니다 <br><b><u>포겟미낫 관리자</u></b>를 통해 접속해주세요<center>')

    # 웹전산에서 회원 리스트를 갱신한다.
    update_member_list(request, aid)

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

    # 모든 학생에 대해 7일간 학습 데이터 가져오기
    member_list = StudyMember.objects.filter(acode=aid)
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
            log_list = StepFinishLog.objects.filter(username=member.mcode, dt_year=yy, dt_month=mm, dt_day=dd).order_by('-id')
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
                    #print(' --' + member.mcode + '/' + str(log.stage) + '/' + str(log.step))
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
        'prev_week': prev_week,
        'next_week': next_week,
        'arg': prev_dt,
        'start_dt': start_dt,
        'days': days,
        'member_list': member_list,
    }
    return render(request, 'manager/week.html', context)


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


