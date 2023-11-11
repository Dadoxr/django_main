from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import SettingCreateView, MessageCreateView, StatisticsMailingView


app_name = MailingConfig.name

urlpatterns = [
    path('setting/', SettingCreateView.as_view(), name='create_setting'),
    path('message/', MessageCreateView.as_view(), name='create_message'),
    path('statistics/', StatisticsMailingView.as_view(), name='statistics'),
 
]