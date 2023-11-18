from django.conf import settings
from django.db import models
from django.utils.timezone import now
from timezone_field import TimeZoneField
from users.models import User


class NameSetting(models.Model):
    """
    Таблица с вариантами ответов полей:
    - period и status в Setting
    """

    category = models.CharField(max_length=255, verbose_name="категория")
    name = models.CharField(max_length=255, verbose_name="вариант")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "вариант"
        verbose_name_plural = "варианты"


class Recipient(models.Model):
    """Получатели рассылки"""

    email = models.EmailField(verbose_name="email")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="владелец"
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "получатель"
        verbose_name_plural = "получатели"


class Message(models.Model):
    """Сообщение для рассылки"""

    subject = models.CharField(max_length=150, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма", blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="владелец"
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "письмо"
        verbose_name_plural = "письма"


class Setting(models.Model):
    """Рассылка (настройки)"""

    start_time = models.TimeField(verbose_name="время рассылки")
    end_time = models.TimeField(verbose_name="конец рассылки", null=True, blank=True)
    time_zone = TimeZoneField(default=settings.TIME_ZONE, verbose_name="часовой пояс")
    period = models.ForeignKey(
        NameSetting,
        on_delete=models.CASCADE,
        limit_choices_to={"category": "periods"},
        verbose_name="периодичность",
        related_name="periods",
    )
    status = models.ForeignKey(
        NameSetting,
        on_delete=models.CASCADE,
        limit_choices_to={"category": "statuses"},
        verbose_name="статус",
        related_name="statuses",
        null=True,
        blank=True,
    )
    recipients = models.ManyToManyField(
        Recipient, verbose_name="получатели", blank=True
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="сообщение", null=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="владелец", null=True, blank=True
    )
    count = models.PositiveIntegerField(default=0, verbose_name="счетчик рассылки")

    def __str__(self):
        return f'{self.period} в {self.start_time.strftime("%H:%M")}'

    class Meta:
        verbose_name = "настройка"
        verbose_name_plural = "настройки"
        ordering = ["start_time"]


class Log(models.Model):
    """Логи рассылки"""

    date_last = models.DateField(auto_now=True, verbose_name="дата последней попытки")
    time_last = models.TimeField(auto_now=True, verbose_name="время последней попытки")
    is_send = models.BooleanField(default=False, verbose_name="статус попытки")
    answer = models.TextField(
        default="init", verbose_name="ответ почтового сервера", null=True, blank=True
    )
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE, verbose_name="лог")

    def __str__(self):
        return f"{self.date_last} {self.time_last}- {self.is_send}"

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"
