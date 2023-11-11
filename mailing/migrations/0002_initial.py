# Generated by Django 4.2.7 on 2023-11-11 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mailing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='setting',
            name='period',
            field=models.ForeignKey(limit_choices_to={'category': 'periods'}, on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='mailing.namesetting', verbose_name='периодичность'),
        ),
        migrations.AddField(
            model_name='setting',
            name='recipients',
            field=models.ManyToManyField(blank=True, to='mailing.recipient', verbose_name='получатели'),
        ),
        migrations.AddField(
            model_name='setting',
            name='status',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'statuses'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='mailing.namesetting', verbose_name='статус'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец'),
        ),
    ]
