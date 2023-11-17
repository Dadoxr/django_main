from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import (
    MessageDeleteView,
    MessageUpdateView,
    SettingCreateView,
    ManageSettingsView,
    ManageMessagesView,
    MessageCreateView,
    SettingDeleteView,
    SettingUpdateView,
    StatisticsMailingView,
    change_status_start_end_setting,
)


app_name = MailingConfig.name

urlpatterns = [
    path("setting/", SettingCreateView.as_view(), name="create_setting"),
    path("setting/<int:pk>", SettingUpdateView.as_view(), name="update_setting"),
    path("setting/<int:pk>/delete", SettingDeleteView.as_view(), name="delete_setting"),
    path("message/", MessageCreateView.as_view(), name="create_message"),
    path("message/<int:pk>", MessageUpdateView.as_view(), name="update_message"),
    path("message/<int:pk>/delete", MessageDeleteView.as_view(), name="delete_message"),
    path("statistics/", StatisticsMailingView.as_view(), name="statistics"),
    path("manage_settings/", ManageSettingsView.as_view(), name="manage_settings"),
    path("manage_messages/", ManageMessagesView.as_view(), name="manage_messages"),
    path("change_status/<int:pk>", change_status_start_end_setting, name="change_status"),
]
