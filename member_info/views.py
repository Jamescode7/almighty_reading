from asyncio import exceptions

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView


def bin_response(request):
    return HttpResponse('bin_response')


def bin_render(request):
    return render(request, 'member_info/bin_render.html')


#fmn을 통해 로그인을 했을 경우, 첫 로그인이라면 이곳에서 새롭게 계정을 생성해준다.
def bin_padding(request):
    get_username = request.GET.get('un')
    get_password = request.GET.get('pw')

    if get_username is not None and get_password is not None:
        if User.objects.filter(username=get_username):
            return HttpResponse('already_create')
        else:
            user = User.objects.create_user(get_username, '', get_password)
            user.save()
            return HttpResponse('create_finish')

    return HttpResponse('test_create')


def del_center(request):
    print('del_center')
    #ZCenter.objects.all().delete() 데이터 모두 삭제. --엑셀 데이터 잘 못 넣었을때 사용함.
    return HttpResponse('ok')



