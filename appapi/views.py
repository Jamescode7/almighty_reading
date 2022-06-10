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
from manager.models import MemberTopicLog, Plan, PlanDetail
from member_info.models import StudyMember
from study_info.models import StepFinishLog, StepTimeLog


def flash_version_check(request):
    ver = AppVersion.objects.filter().order_by('-create_at')[:1]
    ver = ver[0]
    dic = {
        "app_version": str(ver.app_version),
        "download_url": ver.download_url or "",
        "create_at": ver.create_at
    }
    return JsonResponse(dic)


def user_info_load(request):
    mcode = 'userid'

    if request.GET.get('UserID') and request.GET.get('Password'):
        password = request.GET.get('Password')
        user_id = request.GET.get('UserID')
        user_name = request.GET.get('UserName')
        # print('Password : ' + password)
        # print('UserID : ' + user_id)
        # print('user_name : ' + user_name)

        get_user = User.objects.filter(username=user_id)
        if get_user:
            get_user = get_user[0]
            mcode = user_id
        else:
            mcode = user_id
            print('!!!!!user is none!!!!!!! save!')
            print('!! id is :' + user_id )
            user = User.objects.create_user(user_id, '', password)
            user.save()

        get_study_member = StudyMember.objects.filter(mcode=user_id)
        if get_study_member is None:
            get_study_member = get_study_member[0]
            save_study_member = StudyMember(mcode=mcode, mname=user_name, plan_code=Plan.objects.get(plan_code=2))
            save_study_member.save()

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





def common_test(request):
    # https://cem.mrzero.kr/rodata/ca/CommonTest?Time=457537&Mcode=26533
    mcode = request.GET.get('Mcode')

    level_code = "0"
    level_name = ''
    theme_name = ''
    topic_code = "0"
    topic_name = ''


    mem_level = "0"
    mem_level_name = ""
    plan_type = "2"  # 2이면 자유학습, 1이면 플랜학습
    stage = 1
    step = 1
    study_code = 0
    step_code = 0
    step_code_name = ''
    clear_list = []
    plan_name = ''

    user = StudyMember.objects.filter(mcode=mcode)
    if user:
        user = user[0]
        if user.level_code:
            mem_level = str(user.level_code.level_code)
            mem_level_name = user.level_code.level_name
        if user.plan_code:
            plan_type = str(user.plan_code.plan_code)
            plan_name = str(user.plan_code)
        if user.current_study:
            study_code = str(user.current_study)

    if study_code != 0:
        topic_log = MemberTopicLog.objects.get(username=mcode, id=study_code)
        if topic_log:
            level_code = topic_log.level_code.level_code
            level_name = topic_log.level_code.level_name
            topic_code = topic_log.topic_code.topic_code
            topic_name = topic_log.topic_code.topic_name

            theme_code = Topic.objects.get(topic_code=topic_code).theme_code
            theme_name = Theme.objects.get(theme_code=theme_code).theme_name
            stage = topic_log.stage
            step = topic_log.step

            plan_detail = PlanDetail.objects.get(stage=stage, seq=step, plan_code=plan_type)
            if plan_detail:
                step_code = plan_detail.step.step_code
                step_code_name = plan_detail.step.step_name

    if plan_type == "2":
        stage = 1
        step = 1  # 플랜 타입이 자유학습이라면 무조건 스텝과 스테이지는 1로..

    topic_nav = ''
    if level_code == "0" and topic_code == "0":
        # print('라이브러리를 골라야 합니다.')
        history = MemberTopicLog.objects.filter(username=mcode).order_by('-topic_code')
        for row in history:
            # print(str(row))
            clear_list.append(row.topic_code.topic_code)
    else:
        topic_nav = level_name + '>' + theme_name + '>' + topic_name


    data = {
        "Lcode": level_code,
        "Pcode": topic_code,
        "PlanType": plan_type,
        "PlanName": plan_name,
        "LevelLimit": mem_level,
        "LevelLimitName": mem_level_name,
        "Stage": stage,
        "Step": step,
        "StepCode": step_code,
        "StepCodeName": step_code_name,
        "StudyCode": study_code,
        "ClearList": clear_list,
        "TopicNav": topic_nav

    }
    return JsonResponse(data)


###################################################
#
#   L I B R A R Y
#
###################################################


def level_to_dicionary(level, idx):
    dic = {}
    dic["idx"] = str(idx + 1)
    dic["Lcode"] = str(level.level_code)
    dic["Lname"] = level.level_name
    dic["Memo"] = level.memo or ""
    dic["UseYn"] = level.use_yn or ""
    dic["IndexOrder"] = str(level.index_order)
    dic["Total"] = str(level.total)
    return dic


def theme_to_dicionary(theme, idx):
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


def level_theme_load(request):
    # Get level
    level = Level.objects.filter(show_level__gte=2)
    temp_dic = []
    for n in range(len(level)):
        temp_dic.append(level_to_dicionary(level[n], n))
    level = temp_dic

    # Get theme
    theme = Theme.objects.all()
    temp_dic = []
    for n in range(len(theme)):
        temp_dic.append(theme_to_dicionary(theme[n], n))

    theme = temp_dic
    data = {
        "LevelGroup": level,
        "ThemeGroup": theme,
    }
    return JsonResponse(data)


def topic_to_dicionary(topic, idx):
    dic = {
        "idx": str(idx + 1),
        "Pcode": str(topic.topic_code),
        "Tcode": str(topic.theme_code),
        "Pname": topic.topic_name,
        "PreValue": str(topic.pre_value) or "",
        "UseYn": str(topic.use_yn),
        "IndexOrder": str(topic.ord)}
    return dic


def theme_topic_load(request):
    # https://cem.mrzero.kr/rodata/ca/ThemeTopicLoad?Time=1716041&Mcode=26533&Tcode=110&Keyword=
    theme_code = request.GET.get('Tcode')
    topic = Topic.objects.filter(theme_code=theme_code)
    tempDic = []
    for n in range(len(topic)):
        tempDic.append(topic_to_dicionary(topic[n], n))
    topic = tempDic
    data = {
        "TopicGroup": topic,
    }
    return JsonResponse(data)


def topic_select_save(request):
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    level_code = request.GET.get('Lcode')

    topic_code = Topic.objects.get(topic_code=topic_code)
    level_code = Level.objects.get(level_code=level_code)

    # 기존에 다 하지 못한 토픽이 있엇다면 종료 처리.
    topic_list = MemberTopicLog.objects.filter(username=mcode, end_dt=None)
    for topic in topic_list:
        topic.end_dt = datetime.now()
        topic.save()

    # 새로운 토픽 저장.
    save_topic = MemberTopicLog(username=mcode, topic_code=topic_code, level_code=level_code, start_dt=datetime.now(),
                                stage=1, step=1)
    save_topic.save()
    study_code = save_topic.id

    save_study_code = StudyMember.objects.filter(mcode=mcode)
    if save_study_code:
        save_study_code = save_study_code[0]
        save_study_code.current_study = study_code
        save_study_code.save()

    return HttpResponse('save_log_id' + str(study_code))


def word_to_dicionary(word, idx):
    dic = {
        "idx": str(idx + 1),
        "Wcode": str(word.word_code),
        "Pcode": str(word.topic_code),
        "PageNum": str(word.page_num),
        "Num": str(word.num),
        "Eng": str(word.eng),
        "Kor": str(word.kor),
        "DicEng": str(word.dic_eng),
        "DicKor": str(word.dic_kor),
        "Sound": str(word.sound),
        "UseYN": str(word.use_yn)}
    return dic


def wrt_word_to_dicionary(word):
    dic = {
        "Kor": str(word.kor),
        "Eng": str(word.eng),
        "Sound": "http://cem.mrzero.kr/data/SentSound/" + str(word.sound)}
    return dic


def wrt_moon_to_dicionary(topic, idx):
    dic = {
        "idx": str(idx + 1),
        "Rcode": str(topic.reading_code),
        "Pcode": str(topic.topic_code),
        "PageNum": str(topic.page_num),
        "ParaNum": str(topic.para_num),
        "Eng": str(topic.eng),
        "Kor": str(topic.kor)}
    return dic


def topic_main_load(request):
    # https://cem.mrzero.kr/rodata/ca/TopicMainLoad?Time=3415193&Mcode=26533&FlashCode=529647&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    topic = WrtMoon.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(topic)):
        tempDic.append(wrt_moon_to_dicionary(topic[n], n))
    topic = tempDic

    Jimoon = {"Jimoon": topic}

    word = Word.objects.filter(topic_code=topic_code)
    tempWord = []
    for n in range(len(word)):
        tempWord.append(word_to_dicionary(word[n], n))
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
    dic = {
        "Kor": str(spkSent.kor),
        "Eng": str(spkSent.eng),
        "Sound": 'http://fmn2.tongclass.com/reading/data/SentSound/' + str(spkSent.sound)}
    return dic


def speak_sent_load(request):
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


def write_word_load(request):
    # https://cem.mrzero.kr/rodata/ca/WriteWordLoad?Time=4768614&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    wrtWord = WrtWord.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(wrtWord)):
        tempDic.append(wrt_word_to_dicionary(wrtWord[n]))
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


def comp_load(request):
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
def ox_note_load(request):
    # https://cem.mrzero.kr/rodata/ca/OXnoteLoad?Time=5564776&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    pcode = request.GET.get('Pcode')
    data = {}
    return JsonResponse(data)


def get_next_step(get_plan, get_stage, get_step):
    plan_detail = PlanDetail.objects.filter(plan_code=get_plan, stage=get_stage).order_by('seq')
    # print('@@@@@@@@@@@@ g e t _ n e x t _ s t e p @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    return_plan_stage = 0
    return_plan_step = 0
    return_app_step = 0
    return_app_step_name = ''
    return_q_num = 0
    for row in plan_detail:
        # print('-----------------')
        # print('(' + str(row.seq) + ')')
        # print(' ---next stage: ' + str(row.stage))
        # print(' ---next step : ' + str(row.seq))
        # print(' ---next app step : ' + str(row.step.step_code))
        # print(' ---next app step name : ' + str(row.step.step_name))
        if int(get_step) < row.seq:
            # print('!!!! b r e a k - - h e r e!!')
            return_plan_stage = str(row.stage)
            return_plan_step = str(row.seq)
            return_app_step = str(row.step.step_code)
            return_app_step_name = str(row.step.step_name)
            if return_app_step == "6":
                return_q_num = 1
            break

    data = {
        "return_plan_stage": return_plan_stage,
        "return_plan_step": return_plan_step,
        "return_app_step": return_app_step,
        "return_app_step_name": return_app_step_name,
        "return_q_num": return_q_num,
    }
    return data


def step_finish_save(request):
    '''http://127.0.0.1:8080/api/StepFinishSave/?
    Time=55502&
    Mcode=bsp02&        Pcode=76&       StepCode=P01&
    StepNum=0&      Stage=1&        Step=4&
    Cpoint=0&       Tpoint=0&       Ans=null&
    StudyCode=30&       Plan=2&     StudyTime=32
    '''

    is_finish_today = False
    is_finish_topic = False
    return_data = {
        "return_plan_stage": 0,
        "return_plan_step": 0,
        "return_app_step": 0,
        "return_app_step_name": '',
        "return_q_num": 0,
    }

    get_mcode = request.GET.get('Mcode')
    get_topic_code = request.GET.get('Pcode')
    get_step_code = request.GET.get('StepCode')
    get_q_num = request.GET.get('Qnum')
    get_plan = request.GET.get('Plan')
    get_stage = request.GET.get('Stage')
    get_step = request.GET.get('Step')
    get_cpoint = request.GET.get('Cpoint')
    get_tpoint = request.GET.get('Tpoint')
    get_ans = request.GET.get('Ans')
    # studyTime = request.GET.get('StudyTime')
    get_study_code = request.GET.get('StudyCode')

    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    # print('### get data')
    # print('<' + Plan.objects.get(plan_code=get_plan).plan_name + '>')
    # print('stage : ' + get_stage)
    # print('step  : ' + get_step)
    # print('q_num : ' + get_q_num)

    today = date.today()
    year = today.strftime('%y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    # 로그 저장.
    save_topic = StepFinishLog(username=get_mcode, dt_year=year, dt_month=month,
                               dt_day=day, topic_code=get_topic_code, step_code=get_step_code,
                               step_num=str(get_q_num), c_point=get_cpoint, t_point=get_tpoint,
                               answer=get_ans, stage=get_stage, step=get_step, plan_type=get_plan, study_code=get_study_code)
    save_topic.save()

    # 각 변경할 수 있는 정보들 가져오기
    topic_log = MemberTopicLog.objects.get(username=get_mcode, id=get_study_code)
    user = StudyMember.objects.filter(mcode=get_mcode)
    if user:
        user = user[0]

    # 플랜과 스테이지에 해당하는 스텝 가져오기
    return_data = get_next_step(get_plan, get_stage, get_step)

    # 아무것도 안나온다면 오늘 학습할 것이 끝났다는 것이다.
    if return_data['return_app_step_name'] == '':
        # print('오늘 학습 끝!')
        is_finish_today = True

        # 다음에 접속했을때 다음날 학습할 리스트가 있는지 가져온다.
        # print('다음날 학습할 것이 있나요?')
        check_next_stage = int(get_stage) + 1
        check_next_stage = str(check_next_stage)
        return_data = get_next_step(get_plan, check_next_stage, 0)

        # 아무것도 안나온다면 내일 학습할 것도 없으므로 플랜이 끝났다는 것이다.
        # 어쩌면 문제풀이 스텝인 경우-
        if return_data['return_app_step_name'] == '':
            # print('이 플랜의 마지막에 왔습니다!')
            # print('문제 풀이 번호 : ' + get_q_num)
            # print('-----------------')

            return_data['return_q_num'] = int(get_q_num) + 1
            return_data['return_plan_stage'] = str(get_stage)
            return_data['return_plan_step'] = str(get_step)
            return_data['return_app_step'] = "6"
            return_data['return_app_step_name'] = "문제 풀이"
            if get_q_num == '0':
                return_data['return_q_num'] = 0
                is_finish_today = True
                is_finish_topic = True
                return_data['return_app_step_name'] = "토픽 학습 끝"
                topic_log.end_dt = datetime.now()
                user.current_study = 0
                user.save()
            elif get_q_num == '8':
                return_data['return_q_num'] = 0
                is_finish_today = False
                is_finish_topic = False
            else:
                is_finish_today = False
                is_finish_topic = False

            # print(' ---next stage: ' + return_data['return_plan_stage'])
            # print(' ---next step : ' + return_data['return_plan_step'])
            # print(' ---next app step : ' + return_data['return_app_step'])
            # print(' ---next app step name : ' + return_data['return_app_step_name'])

    # print('-----------------')
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    data = {
        "Stage": return_data['return_plan_stage'],
        "Step": return_data['return_plan_step'],
        "StepCode": return_data['return_app_step'],
        "StepCodeName": return_data['return_app_step_name'],
        "FinishToday": is_finish_today,
        "FinishTopic": is_finish_topic,
        "Q_Num": return_data['return_q_num'],
        "StudyCode": get_study_code,
    }

    # print('save check(before) :' + str(topic_log.stage))
    # print('save check(before) :' + str(topic_log.step))
    topic_log.stage = return_data['return_plan_stage']
    topic_log.step = return_data['return_plan_step']
    # print('save check(after) :' + str(topic_log.stage))
    # print('save check(after) :' + str(topic_log.step))
    topic_log.save()
    if is_finish_today:
        save_topic.finish_today = 1
        save_topic.save()

    return JsonResponse(data)


def step_time_save(request):
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
