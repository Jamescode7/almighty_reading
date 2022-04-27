from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from study_info.models import TopicLog


def bin_response(request):
    return HttpResponse('study_info_bin_response')


class StudentListView(ListView):
    pass


class StudentDetailView(DetailView):
    pass


