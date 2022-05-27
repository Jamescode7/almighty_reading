from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView


def bin_response(request):
    return HttpResponse('study_info_bin_response')


class StudentListView(ListView):
    pass


class StudentDetailView(DetailView):
    pass


