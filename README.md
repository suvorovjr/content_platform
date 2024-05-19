# Приложение "Платформа контента"

## Логика работы программы

- Пользлватели могу просматривать бесплатный контент без каких либо ограничений
- Каждый зарегистрированный пользователь сам может стать автором и начать выкладывать как платный, так и бесплатный контент
- Для просмотра платного контента необходимо оплатить подписку
- Реализован функцилнал ленты, подписок на авторов, покупки подписки на платный контент
- На платформе контент двух видов: посты и видео, при этом видел доступны для просмотра на самой 

# Инструкция к приложению "Платформа контента"

## Начало работы

Прежде чем установить проект, вам неободимо убедиться в том, что у Вас:

```
1. Python версии 3.10 или выше
2. Pip для управления зависимостями
```

## 1. Установка зависимостей проекта

Создайте виртуальное окружение с плмлщью команды 
```commandline
python -m venv .venv
```

Активируйте виртуальное окружение с помощью команд:

- Для операционной системы Windows

```commandline
venv/Scripts/activate.bat
```

- Для операционной системы Linux

```commandline
source venv/bin/activate
```

Для установки зависимостей выполните следующую команду:

```commandline
pip install -r requirements.txt
```

## 2. Настройка суперпользователя

Для создания суперпользователя и установки его параметров, отредактируйте файл
`users/management/commands/csu.py`

## 3. Создание суперпользователя

После редактирования для создания суперпользователя в командной строке выполните:

```commandline
python manage.py csu
```

## 4. Настройка переменных окружения

Для работы с перменными необходимо будет создать файл `.env` с вашими данными для
использования БД. Данные для определения указаны в файле `example.env`## 5. Запуск сервера Redis

## 5. Для локального тестирования вебхуков использовался ngrok
Для работы с ним необходимо установить его по иструкции с официального сайта `https://ngrok.com/download`.

После установки запустите ngrok для туннелирования трафика к вашему локальному серверу. Если, например, ваш локальный сервер запущен на порту 8000, выполните следующую команду в командной строке или терминале:
```commandline
ngrok http 8000
```
## 6. Настройки вебхука в Stripe

- Выберите раздел Webhooks (Вебхуки) в боковом меню панели управления Stripe.
- Нажмите на кнопку "Add endpoint" (Добавить точку подключения) или на соответствующую ссылку для создания нового вебхука.
- Скопируйте https-адрес, предоставленный ngrok.
- В поле “Endpoint URL” вставьте URL, предоставленный ngrok, и добавьте путь, который вы сконфигурировали для вебхука в вашем приложении Django.
- В разделе “Events to send” (События для отправки) выберите событие `invoice.payment_succeeded`
- Сохраните созданный вебхук, и Stripe предоставит вам секретный ключ, который пригодится для верификации подписи вебхука, который необходимо добавить в переменные окружения проекта.

# Запуск проекта

После выполнения всех вышеперечисленных шагов вы можете запустить проект с помощью команды:

```commandline
python manage.py runserver
```
# Инструкция по запуску Docker контейнера

Необходимо на хост-компьютере установить Docker для необходимой платформы, скачав его по
адресу https://docs.docker.com/get-docker/

## Запуск

- Войти в учетную запись postgres с помощью команды `sudo -i -u postgres`
  - Создать базу данных с помощью команды `createdb [database_name]`
  - Перейти в консоль postgresql с помощью команды `psql`
    - Создать пользователя с помощью команды `CREATE USER [user_name] WITH PASSWORD 'password';`
    - Дать созданному пользователю права суперпользователя с помощью команды `ALTER USER [user_name] WITH SUPERUSER;`
    - Выйти из консольного режима с помощью команды `\q`
  - Выйти из учетной записи postgres с помощью команды `exit`
- Собрать образ контейнера с помощью команды `docker-compose build`
- Запустить контейнеры с помощью команды `docker-compose up`

