from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import date, timedelta, datetime as dt
from django.views.generic import CreateView, ListView
from mailing import services
from mailing.forms import MessageForm, SettingForm
from mailing.models import Message, NameSetting, Log, Recipient, Setting
from django.db.models import Q


class MessageCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mailing/create.html'
    form_class = MessageForm
    success_url = reverse_lazy('mailing:create_setting')

    def form_valid(self, form):
        if form.data.get('subject'):
            self.object = form.save()
            self.object.owner = self.request.user
            self.object.save()
        return super().form_valid(form)


class SettingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'mailing/create.html'
    form_class = SettingForm
    success_url = reverse_lazy('mailing:statistics')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        created_messages = Message.objects.filter(Q(setting__message__isnull=True), owner=self.request.user) #сообщения юзера не привязанные к настройке
        if created_messages:
            form.fields['message'].queryset = created_messages
        return form

    def form_valid(self, form):
        self.object = form.save()

        #получение объектов юзера из Recipient
        all_recipients_email_list = form.data.get('new_recipients').split(',') + form.data.getlist('old_recipients')
        all_recipients_object_list = services.get_or_create_recipients(all_recipients_email_list, self.request.user)
        
        #обновление полей recipient, status, end_time, owner в Setting
        self.object.recipients.add(*all_recipients_object_list)
        self.object.status = NameSetting.objects.get(name='создана')
        self.object.end_time = (dt.combine(date(1,1,1), self.object.start_time) + timedelta(minutes=10)).time()
        self.object.owner = self.request.user
        
        self.object.save()
        Log.objects.create(setting=self.object).save()

        return super().form_valid(form)
    


class StatisticsMailingView(LoginRequiredMixin, ListView):
    model =  Setting

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        all_user_settings = Setting.objects.filter(owner=self.request.user)
        all_user_recipients = Recipient.objects.filter(owner=self.request.user)

        context_data['count_mailings'] = len(all_user_settings)
        context_data['count_sended_true_mailings'] = len(all_user_settings.filter(log__is_send=True))

        context_data['count_all_recipients'] = len(all_user_recipients)

        return context_data


