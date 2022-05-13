from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from common_value.models import AppVersion


###################################################
#
#   S T A R T
#
###################################################
from library.models import Topic, WrtMoon, Word, SpkSent, Level, Theme, WrtWord, Exam
from member_info.models import TestMember
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
    print('Password : ' + password)
    print('UserID : ' + user_id)
    mcode = 'userid'

    if user_id is not None and password is not None:
        if User.objects.filter(username=user_id):
            mcode = user_id
        else:
            mcode = user_id
            user = User.objects.create_user(user_id, '', password)
            user.save()


    level_code = 0
    topic_code = 0
    if TopicLog.objects.filter(username=user_id).order_by('-select_dt')[:1]:
        row = TopicLog[0]
        row.topic_name


    info = {
        "Mcode": mcode,
        "Mname": mcode,
        "Point": 0,
        "Lcode": 0,
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
    p_code = "0"
    mem_level = "0"

    user = TestMember.objects.filter(mcode=mcode)
    if user:
        print('in user')
        user = user[0]
        mem_level = str(user.level_code.level_code)

    data = {
        "Lcode": mem_level,
        "Pcode": p_code,
    }
    return JsonResponse(data)



###################################################
#
#   L I B R A R Y
#
###################################################


def levelToDicionary(level, idx):
    dic = {}
    dic["idx"] = str(idx+1)
    dic["Lcode"] = str(level.level_code)
    dic["Lname"] = level.level_name
    dic["Memo"] = level.memo or ""
    dic["UseYn"] = level.use_yn or ""
    dic["IndexOrder"] = str(level.index_order)
    dic["Total"] = str(level.total)
    return dic


def themeToDicionary(theme, idx):
    dic = {}
    dic["idx"] = str(idx+1)
    dic["Tcode"] = str(theme.theme_code)
    dic["Lcode"] = str(theme.level_code)
    dic["Tname"] = theme.theme_name
    dic["Memo"] = theme.memo or ""
    dic["UseYn"] = str(theme.use_yn)
    dic["IndexOrder"] = str(theme.ord)
    dic["Total"] = str(theme.total)
    return dic

def levelThemeLoad(request):
    #Get level
    level = Level.objects.all()
    tempDic = []
    for n in range(len(level)):
        tempDic.append(levelToDicionary(level[n], n))
    level = tempDic

    #Get theme
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
    dic["idx"] = str(idx+1)
    dic["Pcode"] = str(topic.topic_code)
    dic["Tcode"] = str(topic.theme_code)
    dic["Pname"] = topic.topic_name
    dic["PreValue"] = str(topic.pre_value) or ""
    dic["UseYn"] = str(topic.use_yn)
    dic["IndexOrder"] = str(topic.ord)
    return dic


def themeTopicLoad(request):
    #https://cem.mrzero.kr/rodata/ca/ThemeTopicLoad?Time=1716041&Mcode=26533&Tcode=110&Keyword=
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
    #https://cem.mrzero.kr/rodata/ca/TopicSelectSave?Time=3414637&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')

    save_topic = TopicLog(username=mcode, topic_code=topic_code)
    save_topic.save()

    return HttpResponse('1')

def wordToDicionary(word, idx):
    dic = {}
    dic["idx"] = str(idx+1)
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
    dic["idx"] = str(idx+1)
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
        tempWord.append(wordToDicionary(word[n],n))
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
    dic["idx"] = str(idx+1)
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
    #https://cem.mrzero.kr/rodata/ca/CompLoad?Time=5301995&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    exam = Exam.objects.filter(topic_code=topic_code)
    tempDic = []
    for n in range(len(exam)):
        tempDic.append(examToDicionary(exam[n], n))
    exam = tempDic

    data = {
        "result": True,
        "type:": "TopicMainLoad",
        "pcode": topic_code,
        "exam": exam,
    }
    return JsonResponse(data)



# 오답노트, 현재 빈 값을 리턴해줌. App에선 사용x
def oXnoteLoad(request):
    #https://cem.mrzero.kr/rodata/ca/OXnoteLoad?Time=5564776&Mcode=26533&Pcode=364
    mcode = request.GET.get('Mcode')
    pcode = request.GET.get('Pcode')
    data = {}
    return JsonResponse(data)


def stepFinishSave(request):
    #https://cem.mrzero.kr/rodata/ca/StepFinishSave?Time=5169391&Mcode=26533&FlashCode=529647&Pcode=364&StepCode=P09&StepNum=0&Cpoint=0&Tpoint=0&Ans=null&StudyTime=24
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    step_code = request.GET.get('StepCode')
    step_num = request.GET.get('StepNum')
    cpoint = request.GET.get('Cpoint')
    tpoint = request.GET.get('Tpoint')
    ans = request.GET.get('Ans')
    studyTime = request.GET.get('StudyTime')

    save_topic = StepFinishLog(username=mcode, topic_code=topic_code, step_code=step_code, step_num=step_num, c_point=cpoint, t_point=tpoint, answer=ans)
    save_topic.save()

    data = {}
    return JsonResponse(data)


def stepTimeSave(request):
    #https://cem.mrzero.kr/rodata/ca/StepTimeSave?Time=46989&Mcode=27462&Pcode=4136&FlashCode=410816&StudyTime=0&StepCode=P01
    mcode = request.GET.get('Mcode')
    topic_code = request.GET.get('Pcode')
    step_code = request.GET.get('StepCode')
    study_time = request.GET.get('StudyTime')
    #https://www.almightyreading.shop/api/StepTimeSave?Time=256619&Mcode=songcheckim&Pcode=364&FlashCode=108142&StudyTime=0&StepCode=P00
    save_topic = StepTimeLog(username=mcode, topic_code=topic_code, step_code=step_code, study_time=study_time)
    save_topic.save()

    data = {}
    return HttpResponse('1')
