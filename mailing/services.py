from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta

from mailing.models import NameSetting, Recipient, Setting, Log


def get_or_create_recipients(all_recipients_email_list, user) -> list:
    """Получение списка объектов получателей с сохранением в БД несуществующих"""

    all_recipients_object_list = []
    for recipient in all_recipients_email_list:
        if "@" in recipient:
            recipient_object = Recipient.objects.get_or_create(
                owner=user, email=recipient.strip()
            )
            recipient_object[0].owner = user
            recipient_object[0].save()
            all_recipients_object_list.append(recipient_object[0])
        elif recipient == "":
            continue
        else:
            recipient_object = Recipient.objects.get(pk=recipient)
            all_recipients_object_list.append(recipient_object)
    return all_recipients_object_list


def create_actual_object_list() -> list:
    """
    Создает список всех объектов Settings, которые пришло время отправлять
    """

    date_now, time_now = now().date(), now().time()
    print(date_now, time_now)

    actual_settings = list(
        Setting.objects.filter(
            start_time__lte=time_now,  # 1) начало >= время сейчас
            end_time__gt=time_now,  # 2) время сейчас < конец
            status__name=settings.NAMESETTING.get("statuses")
            .get("status_create")
            .get("name"),
        )  # 3) статус рассылки: создан
    )

    for period_category, period_values in settings.NAMESETTING.get("periods").items():
        actual_settings += Setting.objects.filter(
            start_time__lte=time_now,  # 1) начало >= время сейчас
            end_time__gt=time_now,  # 2) время сейчас < конец
            status__name__in=[
                settings.NAMESETTING.get("statuses").get("status_start").get("name")
            ],  # 3) статус рассылки: запущена
            period__name=period_values.get(
                "name"
            ),  # 4) периода "раз в день(неделю, месяц)"
            log__date_last=date_now
            - timedelta(
                days=period_values.get("delta_days")
            ),  # 5) последняя рассылка должна быть = сегодня - 1 (7,30)день
        )

    return actual_settings


def check_time_and_send_mail() -> None:
    """
    Формирует список со всеми только что созданными рассылками и добавляет
    рассылки со статусом "завершено" фильтрованные по периоду рассылки.

    Проходит по формированному списку и отправляет сообщение всем получателям, выбранным ранее в
    "создании рассылки" на сайте
    """
    print("Рассылка начата")

    actual_settings = create_actual_object_list()
    count_send_mail = 0

    for mailing_setting in actual_settings:
        count_send_mail += 1
        mailing_setting.status = NameSetting.objects.get(name="запущена")
        mailing_setting.save()

        recipient_emails = [
            recipient.email for recipient in mailing_setting.recipients.all()
        ]

        try:
            success_count = send_mail(
                subject=mailing_setting.message.subject,
                message=mailing_setting.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_emails,
                fail_silently=False,
            )

            is_send = True
            answer = f"Письмо успешно отправлено. Ответ: {success_count}"

        except Exception as e:
            is_send = False
            answer = f"Ошибка отправки: {str(e), success_count}."

        
        Log.objects.create(is_send=is_send, answer=answer, setting=mailing_setting)

        mailing_setting.count += 1
        mailing_setting.save()

    print(f"Рассылка завершена. Выполнено {count_send_mail} рассылок")


def user_is_owner(user, pk, model):
    try:
        object = model.objects.get(pk=pk)
        return object.owner == user
    except model.DoesNotExist:
        return False