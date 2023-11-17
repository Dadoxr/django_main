from django.contrib import admin

from mailing.models import Log, Message, NameSetting, Recipient, Setting

# Register your models here.
admin.site.register(NameSetting)
admin.site.register(Setting)
admin.site.register(Message)
admin.site.register(Recipient)
admin.site.register(Log)
