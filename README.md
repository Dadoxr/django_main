# Django Mailer 'РАЗОШЛИ'

Этот проект представляет собой систему рассылки сообщений по электронной почте с использованием Django. Проект состоит из четырех основных приложений: blog, mailing, users, и main (содержит только главную страницу).

## Установка

1) Убедитесь, что у вас установлен Python3, Redis и Django.

2) Склонируйте репозиторий:
```bash
git clone https://github.com/Dadoxr/django_main.git
cd django_main
```

3) Активируйте виртуальное окружение:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4) Создайте файл `.env` на основе `.env.sample` и заполните его:
```bash
touch django_main/.env
echo django_main/.env.sample > django_main/.env
vim django_main/.env
```

5) Измените `EMAIL_BACKEND` в настройках `django_main/config/settings.py`
```python
# для отправки писем на почту
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# для отправки писем в папку django_main/sent_emails
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
```

6) Создайте базу данных, если ее нет:
```bash
psql -U postgres
CREATE DATABASE DB_NAME;
\q
```

7) Примените миграции:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

8) Создайте все типы юзеров и добавления периодов и статусов в базу данных
- пользователь
- персонал рассылки
- персонал блога
- суперпользователь
+ периоды: 'раз в день', 'раз в неделю', 'раз в месяц'
+ статусы: 'создана', 'запущена', 'завершена', 'отключена'
```bash
python3 manage.py createalltypeusers 
python3 manage.py add_period_statuses
```

9) Запустите сервис:
```bash
python3 manage.py runserver
```

10) Перейдите в `127.0.0.1:8000/admin/auth/group/` и создайте 3 группы с правами
- **blog**:
- - blog.add_blog
- - blog.change_blog
- - blog.delete_blog
- - blog.view_blog
- **staff**:
- - mailing.view_log
- - mailing.view_message
- - mailing.view_setting
- - mailing.view_user
- **user**:
- - blog.view_blog
- - mailing.view_log
- - mailing.add_message
- - mailing.change_message
- - mailing.delete_message
- - mailing.view_message
- - mailing.add_recipient
- - mailing.change_recipient
- - mailing.delete_recipient
- - mailing.view_recipient
- - mailing.add_setting
- - mailing.change_setting
- - mailing.delete_setting
- - mailing.view_setting

11) Добавьте юзеров в группы:
- (blog@blog.blog) в группу blog
- (staff@staff.staff) в группу staff
- (user@user.user) в группу user

12) В отдельном терминале запустите рассылку по расписанию:
```bash
python3 manage.py domailing
```

## Кастомные команды
- `python3 manage.py domailing` - Команда для запуска рассылки по расписанию.
- `python3 manage.py makemailing` - Команда для немедленной отправки рассылки.


## Описание моделей
### `Blog`
Модель представляет блоговые записи.
- `title`: Заголовок блога
- `body`: Текст блога
- `title_image`: Изображение для блога
- `create_at`: Дата создания блога
- `count`: Количество просмотров блога

### `User`
Модель пользователей, расширяющая стандартную модель пользователя Django.
- `email`: Контактный email пользователя
- `confirmation_code`: Код подтверждения
- `comment`: Комментарий пользователя

### `NameSetting`
Таблица с вариантами ответов полей:
- `category`: Категория
- `name`: Вариант

### `Recipient`
Модель для получателей рассылки.
- `email`: Email получателя
- `owner`: Владелец, связанный с моделью User

### `Message`
Модель для сообщений рассылки.
- `subject`: Тема письма
- `body`: Текст письма
- `owner`: Владелец, связанный с моделью User

### `Setting`
Модель для настроек рассылки.
- `start_time`: Время начала рассылки
- `end_time`: Время окончания рассылки
- `time_zone`: Часовой пояс
- `period`: Периодичность, связанная с моделью NameSetting
- `status`: Статус, связанный с моделью NameSetting
- `recipients`: Множество получателей, связанных с моделью Recipient
- `message`: Сообщение, связанное с моделью Message
- `owner`: Владелец, связанный с моделью User
- `count`: Счетчик рассылки

### `Log`
Модель для логов рассылки.
- `date_last`: Дата последней попытки
- `time_last`: Время последней попытки
- `is_send`: Статус попытки
- `answer`: Ответ почтового сервера
- `setting`: Связанная с моделью Setting


## Ссылки на сайт:
- 127.0.0.1:8000/ - Главная страница
- 127.0.0.1:8000/admin/ - Админ панель

- 127.0.0.1:8000/users/ - Вход в систему
- 127.0.0.1:8000/users/logout/ - Выход из системы
- 127.0.0.1:8000/users/register/ - Регистраци в системе
- 127.0.0.1:8000/users/profile/ - Изменения данных профиля
- 127.0.0.1:8000/users/list/ - Список всех пользователей, кроме is_staff, is_superuser

- 127.0.0.1:8000/mailing/setting - Создать рассылку
- 127.0.0.1:8000/mailing/message - Создать сообщение
- 127.0.0.1:8000/mailing/statistics - Логи рассылки
- 127.0.0.1:8000/mailing/manage_settings - Список рассылок 
- 127.0.0.1:8000/mailing/manage_messages - Список сообщений

- 127.0.0.1:8000/blog/ - Список всех статей 
