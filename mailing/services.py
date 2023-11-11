from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta

from mailing.models import NameSetting, Recipient, Setting, Log


def get_or_create_recipients(all_recipients_email_list, user) -> list:
    ''' Получение списка объектов получателей с сохранением в БД несуществующих '''

    all_recipients_object_list = []
    for recipient in all_recipients_email_list:
        if '@' in recipient:
            recipient_object = Recipient.objects.get_or_create(owner=user, email=recipient.strip())
            recipient_object[0].owner = user
            recipient_object[0].save()
            all_recipients_object_list.append(recipient_object[0])
        elif recipient == '':
            continue
        else:
            recipient_object = Recipient.objects.get(pk=recipient)
            all_recipients_object_list.append(recipient_object)
    return all_recipients_object_list


def check_time_and_send_mail() -> None:
    '''
        Формирует список со всеми только что созданными рассылками и добавляет
        рассылки со статусом "завершено" фильтрованные по периоду рассылки.

        Проходит по формированному списку и отправляет сообщение всем получателям, выбранным ранее в 
        "создании рассылки" на сайте
    '''

    time_now, date_now = now().time(), now().date()
    
    actual_settings = list(
        Setting.objects.filter(status__name=settings.NAMESETTING.get('statuses').get('status_create').get('name'))
    ) # список только что созданных (необбработанных) рассылок

    for period_category, period_values in settings.NAMESETTING.get('periods').items():
        actual_settings += Setting.objects.filter(
            start_time__lte=time_now, # 1) начало >= время сейчас
            end_time__gt=time_now,  # 2) время сейчас < конец
            status__name__in=[settings.NAMESETTING.get('statuses').get('status_end').get('name')], # 3) статус рассылки: завершен
            period__name=period_values.get('name'), # 4) периода "раз в день(неделю, месяц)"
            log__date_last=date_now - timedelta(days=period_values.get('delta_days')), # 5) последняя рассылка должна быть = сегодня - 1 (7,30)день
        )
    
    for mailing_setting in actual_settings:
        mailing_setting.status = NameSetting.objects.get(name='запущена')
        mailing_setting.save()

        recipient_emails = [recipient.email for recipient in mailing_setting.recipients.all()]

        try:
            success_count = send_mail(
                subject=mailing_setting.message.subject,
                message=mailing_setting.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_emails
            )

            mailing_setting.log.is_send = True
            mailing_setting.log.answer = f"Письмо успешно отправлено {success_count} раз."

        except Exception as e:
            mailing_setting.log.is_send = False
            mailing_setting.log.answer = f"Ошибка отправки: {str(e)}"

        finally:
            mailing_setting.log.save()

            mailing_setting.status = NameSetting.objects.get(name='завершена')
            mailing_setting.save()