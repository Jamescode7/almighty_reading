from django.shortcuts import render

def fmn_privacy_policy_view(request):
    return render(request, 'engedu_privacy_policy/fmn_privacy_policy.html')
