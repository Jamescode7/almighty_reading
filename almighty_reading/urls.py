"""almighty_reading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from django.shortcuts import redirect

from django.views.static import serve
import os

from common_value.models import AppVersion
from manage import main
from study_info.views import bin_response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEP_READING = os.path.join(BASE_DIR, 'step_reading')
STEP_READING2 = os.path.join(BASE_DIR, 'step_reading2')
STEP_READING3 = os.path.join(BASE_DIR, 'step_reading3')
STEP_READING4 = os.path.join(BASE_DIR, 'step_reading4')

def step_reading(request, resource):
    return serve(request, resource, STEP_READING)
def step_reading2(request, resource):
    return serve(request, resource, STEP_READING2)
def step_reading3(request, resource):
    return serve(request, resource, STEP_READING3)
def step_reading4(request, resource):
    return serve(request, resource, STEP_READING4)

urlpatterns = [
    path('', lambda request: redirect('manager/info/', permanent=False)),
    path('ad/adm/admin/', admin.site.urls),
    path('member_info/', include('member_info.urls')),
    path('library/', include('library.urls')),
    path('common_value/', include('common_value.urls')),
    path('study_info/', include('study_info.urls')),
    path('api/', include('appapi.urls')),
    path('manager/', include('manager.urls')),
    path('dialog/', include('dialog.urls')),
    path('engedu_privacy_policy/', include('engedu_privacy_policy.urls')),

    #path('step_reading/', lambda r: flutter_redirect(r, 'index.html')),
    #path('step_reading/<path:resource>', flutter_redirect),
]
'''
urlpatterns = [
    path('', lambda request: redirect('manager/info/', permanent=False)),
    path('ad/adm/admin/', admin.site.urls),
    path('member_info/', include('member_info.urls')),
    path('library/', include('library.urls')),
    path('common_value/', include('common_value.urls')),
    path('study_info/', include('study_info.urls')),
    path('api/', include('appapi.urls')),
    path('manager/', include('manager.urls')),
    path('dialog/', include('dialog.urls')),

    path('step_reading/', lambda r: flutter_redirect(r, 'index.html')),
    path('step_reading/<path:resource>', flutter_redirect),
]
'''

'''
urlpatterns = [
    path('', lambda request: redirect('step_reading/', permanent=False)),
    path('step_reading/', lambda r: step_reading(r, 'index.html')),
    path('step_reading/<path:resource>', step_reading),

    path('step_reading2/', lambda r: step_reading2(r, 'index.html')),
    path('step_reading2/<path:resource>', step_reading2),

    path('step_reading3/', lambda r: step_reading3(r, 'index.html')),
    path('step_reading3/<path:resource>', step_reading3),

    path('step_reading4/', lambda r: step_reading4(r, 'index.html')),
    path('step_reading4/<path:resource>', step_reading4),
]
'''