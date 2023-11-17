from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from datetime import date, timedelta, datetime as dt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from mailing import services
from mailing.forms import MessageForm, SettingForm
from mailing.models import Message, NameSetting, Log, Setting
from django.db.models import Q


@login_required
def change_status_start_end_setting(request, pk):
    """
    Меняет статус рассылки, предварительно проверяя кто запросил изменение user или staff.
    Для Staff -> блокирует рассылку для user и дальнейшей рассылки
    Для User -> отключает рассылку с возможностью включить
    """

    setting_object = get_object_or_404(Setting, pk=pk)

    statuses = settings.NAMESETTING.get("statuses")

    status_create = statuses.get("status_create").get("name")
    status_start = statuses.get("status_start").get("name")
    status_end = statuses.get("status_end").get("name")
    status_stop = statuses.get("status_stop").get("name")

    if request.user.is_staff:
        if setting_object.status.name == status_stop:
            setting_object.status = NameSetting.objects.get(name=status_start)
        else:
            setting_object.status = NameSetting.objects.get(name=status_stop)
    else:
        if setting_object.status.name in (status_start, status_create):
            setting_object.status = NameSetting.objects.get(name=status_end)
        elif setting_object.status.name == status_end:
            setting_object.status = NameSetting.objects.get(name=status_start)
        else:
            raise Http404
    setting_object.save()
    return redirect(reverse("mailing:manage_settings"))


##### MESSAGE #####
class MessageCreateView(LoginRequiredMixin, CreateView):
    template_name = "mailing/create_message.html"
    form_class = MessageForm
    success_url = reverse_lazy("mailing:create_setting")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Сообщение",
        "description": "Создание сообщения рассылки",
    }

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    template_name = "mailing/update_message.html"
    fields = (
        "subject",
        "body",
    )
    success_url = reverse_lazy("mailing:manage_messages")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Сообщение",
        "description": "Создание сообщения рассылки",
    }

    def test_func(self):
        return services.user_is_owner(self.request.user, self.kwargs["pk"], Message)


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:manage_messages")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Удаление",
        "description": "Подтвердите удаление сообщение (настройка рассылки этого сообщения так же удалится)",
    }

    def test_func(self):
        return services.user_is_owner(self.request.user, self.kwargs["pk"], Message)


class ManageMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/manage_messages.html"
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Управление сообщениями",
        "description": "Здесь вы можете изменять сообщения и удалять их",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset




##### SETTING #####
class SettingCreateView(LoginRequiredMixin, CreateView):
    template_name = "mailing/create_setting.html"
    form_class = SettingForm
    success_url = reverse_lazy("mailing:statistics")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Настройка",
        "description": "Создание настройки рассылки",
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        created_messages = Message.objects.filter(
            Q(setting__message__isnull=True), owner=self.request.user
        )  # сообщения юзера не привязанные к настройке
        if created_messages:
            form.fields["message"].queryset = created_messages
        return form

    def form_valid(self, form):
        self.object = form.save()

        # получение объектов юзера из Recipient
        all_recipients_email_list = form.data.get("new_recipients").split(
            ","
        ) + form.data.getlist("old_recipients")
        all_recipients_object_list = services.get_or_create_recipients(
            all_recipients_email_list, self.request.user
        )

        # обновление полей recipient, status, end_time, owner в Setting
        self.object.recipients.add(*all_recipients_object_list)
        self.object.status = NameSetting.objects.get(name="создана")
        self.object.end_time = (dt.combine(date(1, 1, 1), self.object.start_time) + timedelta(minutes=10)).time()
        self.object.owner = self.request.user

        self.object.save()

        return super().form_valid(form)


class SettingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Setting
    template_name = "mailing/update_setting.html"
    fields = (
        "start_time",
        "period",
        "recipients",
        "message",
    )
    success_url = reverse_lazy("mailing:manage_settings")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Сообщение",
        "description": "Изменение сообщения рассылки",
    }

    def test_func(self):
        return services.user_is_owner(self.request.user, self.kwargs["pk"], Setting)


class SettingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Setting
    success_url = reverse_lazy("mailing:manage_settings")
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Удаление",
        "description": "Подтвердите удаление рассылки",
    }

    def test_func(self):
        return services.user_is_owner(self.request.user, self.kwargs["pk"], Setting)


class ManageSettingsView(LoginRequiredMixin, ListView):
    model = Setting
    template_name = "mailing/manage_settings.html"
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Управление рассылками",
        "description": "Здесь вы можете изменять рассылки, отменять и удалять их",
        "status_end": settings.NAMESETTING.get("statuses").get("status_end").get("name"),
        "status_stop": settings.NAMESETTING.get("statuses").get("status_stop").get("name"),
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


##### LOG #####
class StatisticsMailingView(LoginRequiredMixin, ListView):
    model = Log
    template_name = "mailing/statistics.html"
    extra_context = {
        "site_name": settings.SITE_NAME,
        "title": "Статистика",
        "description": "Вся информация о рассылках",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(setting__owner=self.request.user)
        return queryset