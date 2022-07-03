from django.shortcuts import render

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

    context = {
        'sound_path': 'http://fmn2.tongclass.com/reading_dialog/',
        'step_list': step_list,
        'step_code': step_code,
        'bookcd_list': bookcd_list,
        'bookcd_code': bookcd_code,
        'track_list': track_list,
    }
    return render(request, 'dialog/dialog.html', context)
