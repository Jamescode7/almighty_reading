from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from library.models import Level
from manager.models import Plan, MemberTopicLog
from member_info.models import TestMember


def manager_list(request):
    member_list = TestMember.objects.filter(acode='C72240')
    context = {
        'member_list': member_list,
    }
    return render(request, 'manager/manager_list.html', context)


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


def dashboard(request):
    return render(request, 'manager/dashboard.html')


def basic_table(request):
    return render(request, 'manager/basic-table.html')

def profile(request):
    return render(request, 'manager/profile.html')


