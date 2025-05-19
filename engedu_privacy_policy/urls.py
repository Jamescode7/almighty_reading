from django.urls import path
from .views import fmn_privacy_policy_view

app_name = 'engedu_privacy_policy'

urlpatterns = [
    path('forget_me_not', fmn_privacy_policy_view, name='fmn_privacy_policy_view'),
]
