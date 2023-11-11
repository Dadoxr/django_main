# Generated by Django 4.2.7 on 2023-11-11 14:47

from django.db import migrations, models
import django.db.models.deletion
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last', models.DateField(auto_now=True, verbose_name='дата последней попытки')),
                ('time_last', models.TimeField(auto_now=True, verbose_name='время последней попытки')),
                ('is_send', models.BooleanField(default=False, verbose_name='статус попытки')),
                ('answer', models.TextField(blank=True, default='init', null=True, verbose_name='ответ почтового сервера')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=150, verbose_name='тема письма')),
                ('body', models.TextField(blank=True, verbose_name='тело письма')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
            },
        ),
        migrations.CreateModel(
            name='NameSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, verbose_name='категория')),
                ('name', models.CharField(max_length=255, verbose_name='вариант')),
            ],
            options={
                'verbose_name': 'вариант',
                'verbose_name_plural': 'варианты',
            },
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
            ],
            options={
                'verbose_name': 'получатель',
                'verbose_name_plural': 'получатели',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(verbose_name='время рассылки')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='конец рассылки')),
                ('time_zone', timezone_field.fields.TimeZoneField(default='UTC', verbose_name='часовой пояс')),
                ('log', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.log', verbose_name='лог')),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'настройка',
                'verbose_name_plural': 'настройки',
            },
        ),
    ]