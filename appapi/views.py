from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from common_value.models import AppVersion
from datetime import date, timedelta, datetime

###################################################
#
#   S T A R T
#
###################################################
from library.models import Topic, WrtMoon, Word, SpkSent, Level, Theme, WrtWord, Exam
from manager.models import MemberTopicLog, Plan
from member_info.models import StudyMember
from study_info.models import TopicLog, StepFinishLog, StepTimeLog


def version_dic(version):
    dic = {}
    dic["app_version"] = str(version.app_version)
    dic["download_url"] = version.download_url or ""
    dic["create_at"] = version.create_at
    return dic


def flash_version_check(request):
    ver = AppVersion.objects.filter().order_by('-create_at')[:1]
    ver = version_dic(ver[0])
    return JsonResponse(ver)


def user_info_load(request):
    # https://cem.mrzero.kr/rodata/ca/UserInfoLoad?Password=hello&UserID=cem&dummy=1650007104221
    password = request.GET.get('Password')
    user_id = request.GET.get('UserID')
    user_name = request.GET.get('UserName')
    print('Password : ' + password)
    print('UserID : ' + user_id)
    print('user_name : ' + user_name)
    mcode = 'userid'

    if user_id is not None and password is not None:
        if User.objects.filter(username=user_id):
            mcode = user_id
        else:
            mcode = user_id

            # User에 저장. User의 username에 ID를 고유하게 사용한다.
            user = User.objects.create_user(user_id, '', password)
            user.save()

            # StudyMember에서도 저장.
            save_study_member = StudyMember(mcode=mcode, mname=user_name, plan_code=Plan.objects.get(plan_code=2))
            save_study_member.save()


    level_code = 0
    topic_code = 0

    info = {
        "Mcode": mcode,
        "Mname": mcode,
        "Point": 0,
        "Lcode": 100,  # 여기서의 Lcode값은 의미가 없고..CommonTest에서의 Lcode가 최종 값.
        "Pcode": 0,
        "Pname": "",
        "Tcp": "",
        "Tlp": "",
        "ChangeSw": "1",
        "DoCheck": "0",
        "DayPoint": "0",
        "Gubun": "",
        "UseOrder": "",
        "UserKind": "M0",
        "PointBlank": "",
        "PointSent": "",
        "PointExam": "",
        "MinusPointBlank": "",
        "StepCode": "",
        "StudyKind": []
    }
    data = {
        "Info": info,
    }
    return JsonResponse(data)


def get_topic_log(user_name):
    topic_log = MemberTopicLog.objects.filter(username=user_name, end_dt=None).order_by('-id')
    if topic_log:
        topic_log = topic_log[0]
        return topic_log


def common_test(request):
    # https://cem.mrzero.kr/rodata/ca/CommonTest?Time=457537&Mcode=26533
    mcode = request.GET.get('Mcode')

    level_code = "0"
    topic_code = "0"

    mem_level = "0"
    plan_type = "2"  # 2이면 자유학습, 1이면 플랜학습
    stage = 1
    step = 1

    user = StudyMember.objects.filter(mcode=mcode)
    if user:
        user = user[0]
        if user.level_code:
            mem_level = str(user.level_code.level_code)
        if user.plan_code:
            plan_type = str(user.plan_code.plan_code)

    topic_log = get_topic_log(mcode)
    if topic_log:
        level_code = topic_log.level_code.level_code
        topic_code = topic_log.topic_code.topic_code
        stage = topic_log.stage
        step = topic_log.step

    if plan_type == "2":
        stage = 1
        step = 1  # 플랜 타입이 자유학습이라면 무조건 스텝과 스테이지는 1로..

    data = {
        "Lcode": level_code,
        "Pcode": topic_code,
        "PlanType": plan_type,
        "LevelLimit": mem_level,
        "Stage": stage,
        "Step": step,
    }
    return JsonResponse(data)


###################################################
#
#   L I B R A R Y
#
###################################################


def levelToDicionary(level, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Lcode"] = str(level.level_code)
    dic["Lname"] = level.level_name
    dic["Memo"] = level.memo or ""
    dic["UseYn"] = level.use_yn or ""
    dic["IndexOrder"] = str(level.index_order)
    dic["Total"] = str(level.total)
    return dic


def themeToDicionary(theme, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Tcode"] = str(theme.theme_code)
    dic["Lcode"] = str(theme.level_code)
    dic["Tname"] = theme.theme_name
    dic["Memo"] = theme.memo or ""
    dic["UseYn"] = str(theme.use_yn)
    dic["IndexOrder"] = str(theme.ord)
    #dic["Total"] = str(theme.total)
    topic = Topic.objects.filter(theme_code=theme.theme_code)
    child = str(topic.count())
    dic["Total"] = child
    return dic


def levelThemeLoad(request):
    # Get level
    level = Level.objects.all()
    tempDic = []
    for n in range(len(level)):
        tempDic.append(levelToDicionary(level[n], n))
    level = tempDic

    # Get theme
    theme = Theme.objects.all()
    tempDic = []
    for n in range(len(theme)):
        tempDic.append(themeToDicionary(theme[n], n))

    theme = tempDic
    data = {
        "LevelGroup": level,
        "ThemeGroup": theme,
    }
    return JsonResponse(data)


def topicToDicionary(topic, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Pcode"] = str(topic.topic_code)
    dic["Tcode"] = str(topic.theme_code)
    dic["Pname"] = topic.topic_name
    dic["PreValue"] = str(topic.pre_value) or ""
    dic["UseYn"] = str(topic.use_yn)
    dic["IndexOrder"] = str(topic.ord)
    return dic


def themeTopicLoad(request):
    # https://cem.mrzero.kr/rodata/ca/ThemeTopicLoad?Time=1716041&Mcode=26533&Tcode=110&Keyword=
    theme_code = request.GET.get('Tcode')
    topic = Topic.objects.filter(theme_code=theme_code)
    tempDic = []
    for n in range(len(topic)):
        tempDic.append(topicToDicionary(topic[n], n))
    topic = tempDic
    data = {
        "TopicGroup": topic,
    }
    return JsonResponse(data)


def topicSelectSave(request):
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    level_code = request.GET.get('Lcode')

    topic_code = Topic.objects.get(topic_code=topic_code)
    level_code = Level.objects.get(level_code=level_code)

    # 기존에 다 하지 못한 토픽이 있엇다면 종료 처리.
    topic_log = get_topic_log(mcode)
    if topic_log:
        topic_log.end_dt = datetime.now()
        topic_log.save()

    # 새로운 토픽 저장.
    save_topic = MemberTopicLog(username=mcode, topic_code=topic_code, level_code=level_code, start_dt=datetime.now(),
                                stage=1, step=1)
    save_topic.save()

    return HttpResponse('1')


def wordToDicionary(word, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Wcode"] = str(word.word_code)
    dic["Pcode"] = str(word.topic_code)
    dic["PageNum"] = str(word.page_num)
    dic["Num"] = str(word.num)
    dic["Eng"] = str(word.eng)
    dic["Kor"] = str(word.kor)
    dic["DicEng"] = str(word.dic_eng)
    dic["DicKor"] = str(word.dic_kor)
    dic["Sound"] = str(word.sound)
    dic["UseYN"] = str(word.use_yn)
    return dic


def wrtWordToDicionary(word):
    dic = {}
    dic["Kor"] = str(word.kor)
    dic["Eng"] = str(word.eng)
    dic["Sound"] = "http://cem.mrzero.kr/data/SentSound/" + str(word.sound)
    return dic


def wrtMoonToDicionary(topic, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Rcode"] = str(topic.reading_code)
    dic["Pcode"] = str(topic.topic_code)
    dic["PageNum"] = str(topic.page_num)
    dic["ParaNum"] = str(topic.para_num)
    dic["Eng"] = str(topic.eng)
    dic["Kor"] = str(topic.kor)
    return dic


def topicMainLoad(request):
    # https://cem.mrzero.kr/rodata/ca/TopicMainLoad?Time=3415193&Mcode=26533&FlashCode=529647&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    topic = WrtMoon.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(topic)):
        tempDic.append(wrtMoonToDicionary(topic[n], n))
    topic = tempDic

    Jimoon = {"Jimoon": topic}

    word = Word.objects.filter(topic_code=topic_code)
    tempWord = []
    for n in range(len(word)):
        tempWord.append(wordToDicionary(word[n], n))
    word = tempWord
    WordBook = {"WordBook": word}

    root = []
    root.append(Jimoon)
    root.append(WordBook)

    data = {
        "result": True,
        "type": "TopicMainLoad",
        "pcode": str(topic_code),
        "Root": root,
    }
    return JsonResponse(data)


def spkSentToDicionary(spkSent):
    dic = {}
    dic["Kor"] = str(spkSent.kor)
    dic["Eng"] = str(spkSent.eng)
    dic["Sound"] = 'http://fmn2.tongclass.com/reading/data/SentSound/' + str(spkSent.sound)
    return dic


def speakSentLoad(request):
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    spkSent = SpkSent.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(spkSent)):
        tempDic.append(spkSentToDicionary(spkSent[n]))
    spkSent = tempDic

    data = {
        "result": True,
        "data": spkSent,
    }
    return JsonResponse(data)


def writeWordLoad(request):
    # https://cem.mrzero.kr/rodata/ca/WriteWordLoad?Time=4768614&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    wrtWord = WrtWord.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(wrtWord)):
        tempDic.append(wrtWordToDicionary(wrtWord[n]))
    wrtWord = tempDic

    data = {
        "result": True,
        "data": wrtWord,
    }
    return JsonResponse(data)


# Process2 API
def examToDicionary(exam, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Pcode"] = str(exam.topic_code)
    dic["Num"] = str(exam.num)
    dic["ParaNum"] = str(exam.para_num)
    dic["Kind"] = str(exam.kind)
    dic["Ask"] = str(exam.ask)
    dic["Ans"] = str(exam.answer)
    dic["S1"] = exam.s1 or ""
    dic["S2"] = exam.s2 or ""
    dic["S3"] = exam.s3 or ""
    dic["S4"] = exam.s4 or ""
    dic["S5"] = exam.s5 or ""
    return dic


def compLoad(request):
    # https://cem.mrzero.kr/rodata/ca/CompLoad?Time=5301995&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    exam = Exam.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(exam)):
        tempDic.append(examToDicionary(exam[n], n))
    exam = tempDic

    data = {
        "result": True,
        "type": "TopicMainLoad",
        "pcode": topic_code,
        "exam": exam,
    }
    return JsonResponse(data)


# 오답노트, 현재 빈 값을 리턴해줌. App에선 사용x
def oXnoteLoad(request):
    # https://cem.mrzero.kr/rodata/ca/OXnoteLoad?Time=5564776&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    pcode = request.GET.get('Pcode')
    data = {}
    return JsonResponse(data)


def stepFinishSave(request):
    # https://cem.mrzero.kr/rodata/ca/StepFinishSave?Time=5169391&Mcode=26533&FlashCode=529647&Pcode=364&StepCode=P09&StepNum=0&Cpoint=0&Tpoint=0&Ans=null&StudyTime=24
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    step_code = request.GET.get('StepCode')
    q_num = request.GET.get('StepNum')
    stage = request.GET.get('Stage')
    step = request.GET.get('Step')

    cpoint = request.GET.get('Cpoint')
    tpoint = request.GET.get('Tpoint')
    ans = request.GET.get('Ans')
    studyTime = request.GET.get('StudyTime')
    plan_type = 0
    is_finish_today = False
    is_finish_topic = False

    today = date.today()
    year = today.strftime('%y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    save_topic = StepFinishLog(username=mcode, dt_year=year, dt_month=month,
                               dt_day=day, topic_code=topic_code, step_code=step_code,
                               step_num=str(q_num), c_point=cpoint, t_point=tpoint,
                               answer=ans, stage=stage, step=step)
    save_topic.save()

    # Next Step, Stage, Plan
    topic_log = get_topic_log(mcode)
    if topic_log:
        step = topic_log.step
        stage = topic_log.stage

    user = StudyMember.objects.filter(mcode=mcode)
    if user:
        user = user[0]
        if user.plan_code:
            plan_type = str(user.plan_code.plan_code)

    # Flow plan
    #  <PLAN 1 - 완전학습>
    #  첫 날 -Stage1 /1.듣고 따라하기-Step1 / 2.문장말하기-Step2
    #  둘째날 -Stage2 /1. 문단말하기-Step1 / 2. 빈칸 채우기-Step2
    #  셋째날 -Stage3 / 1. 직독직해-Step1 / 2. 문단말하기-Step2 / 3. 프로세스 2의 문제 풀이-Step3

    print('=============')
    print('plan : ' + plan_type)
    print('stage : ' + str(stage))
    print('step : ' + str(step))
    print('q_num : ' + str(q_num))
    print('------->>')
    if plan_type == '1':  # 완전학습
        if stage == 1 or stage == 2:
            if step < 2:
                step += 1
            else:
                stage += 1
                step = 1
                is_finish_today = True
        elif stage == 3:
            if step < 3:
                step += 1
            elif step == 3:
                q_num = int(q_num)
                if q_num == 0:
                    is_finish_topic = True
                    topic_log.end_dt = datetime.now()
                else:
                    q_num += 1
    elif plan_type == '2':  # 자유학습
        step += 1
        if step == 7:
            step = 1

    topic_log.stage = stage
    topic_log.step = step
    topic_log.save()
    print('stage : ' + str(stage))
    print('step : ' + str(step))
    data = {
        "Stage": stage,
        "Step": step,
        "FinishToday": is_finish_today,
        "FinishTopic": is_finish_topic,
        "Q_Num": q_num,
    }
    return JsonResponse(data)


def stepTimeSave(request):
    # https://cem.mrzero.kr/rodata/ca/StepTimeSave?Time=46989&Mcode=27462&Pcode=4136&FlashCode=410816&StudyTime=0&StepCode=P01
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    step_code = request.GET.get('StepCode')
    study_time = request.GET.get('StudyTime')
    # https://www.almightyreading.shop/api/StepTimeSave?Time=256619&Mcode=songcheckim&Pcode=364&FlashCode=108142&StudyTime=0&StepCode=P00
    save_topic = StepTimeLog(username=mcode, topic_code=topic_code, step_code=step_code, study_time=study_time)
    save_topic.save()

    data = {}
    return HttpResponse('1')
