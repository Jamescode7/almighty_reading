from django.http import HttpResponse
from django.shortcuts import render

from common_value.models import EtcValue
from dialog.models import Dialog


def main(request):
    step_list = []
    step_code = ''
    bookcd_list = []
    bookcd_code = ''
    track_list = []

    all_list = Dialog.objects.all()
    all_list = all_list.values_list('name', flat=True).distinct()
    for row in all_list:
        step_list.append(row)

    if request.GET.get('step'):
        step_code = request.GET.get('step')
        if step_code == 'Freeway S2':
            all_list = Dialog.objects.filter(name=step_code).order_by('book_cd')
        else:
            all_list = Dialog.objects.filter(name=step_code)
        all_list = all_list.values_list('book_cd', flat=True).distinct()
        for row in all_list:
            book_cd = {}
            book_cd['value'] = row
            row = row.replace('_', '권 ')
            book_cd['name'] = row
            bookcd_list.append(book_cd)

        if request.GET.get('bookcd'):
            bookcd_code = request.GET.get('bookcd')
            track_list = Dialog.objects.filter(name=step_code, book_cd=bookcd_code)
            for track in track_list:
                track.mp3 = track.step + '_' + track.book_cd + '_' + str(track.track) + '.mp3'

    dialog_audio_play_popup = 0
    etc_value_list = EtcValue.objects.all()
    for etc_value in etc_value_list:
        if etc_value.etc_name == 'DIALOG_AUDIO_PLAY_POPUP':
            dialog_audio_play_popup = etc_value.etc_value

    context = {
        'dialog_audio_play_popup': dialog_audio_play_popup,
        'sound_path': 'http://fmn2.tongclass.com/reading_dialog/',
        'step_list': step_list,
        'step_code': step_code,
        'bookcd_list': bookcd_list,
        'bookcd_code': bookcd_code,
        'track_list': track_list,
    }
    return render(request, 'dialog/dialog.html', context)


def audio(request):
    if request.GET:
        step_code = request.GET.get('step_code')
        bookcd_code = request.GET.get('bookcd_code')
        track_idx = request.GET.get('track_idx')
        track_list = Dialog.objects.filter(name=step_code, book_cd=bookcd_code)
        step_name = ''
        book_cd = ''
        for track in track_list:
            step_name = track.name
            book_cd = track.book_cd
            track.mp3 = "http://fmn2.tongclass.com/reading_dialog/" + track.step + '_' + track.book_cd + '_' + str(track.track) + '.mp3'

        book_cd = book_cd.replace('_', '권 CD-')
        context = {
            'track_idx': track_idx,
            'step_name': step_name,
            'book_cd': book_cd,
            'track_list': track_list,
        }
        return render(request, 'dialog/audio.html', context)
    return HttpResponse('잘못된 접근입니다')
