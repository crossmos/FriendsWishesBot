# FriednsWishesBot
Telegram-бот, который помогает хранить список желаний, и следить за списками своих друзей.

## Используемый стэк
1. Django REST Framework
2. pyTelegramBot
3. Docker compose

## Как запустить проект с помощью Docker compose
1. Создать бот через @BotFather и получить токен этого бота
2. Переименовать файл ".env-template" в ".env" и заполнить переменные
3. Открываем файл "constants.py" в директории bot_v2 и устанавливаем значение DOCKER_STATUS=True
4. Запускаем Docker и находясь в директории wish_list_bot выполняем команду
```
docker compose up --build
``` 

## Как запустить проект локально
1. Создать бот через @BotFather и получить токен этого бота
2. Переименовать файл ".env-template" в ".env" и заполнить переменные
3. Открываем файл "constants.py" в директории bot_v2 и устанавливаем значение DOCKER_STATUS=False
4. Установить и запустить вирутальное окружение

```
python -m venv venv
```
```
source venv/Scripts/activate
```

или

```
python3 -m venv venv
```
```
source venv/bin/activate
```

4. Перейти в директорию wish_list/ и запустить сервер
```
cd wish_list/
```
```
python manage.py runserver
```

или

```
cd wish_list/
```
```
python3 manage.py runserver
```

5. Перейти в директорию bot_v2/ и запустить скрипт main.py
```
cd bot/
```
```
python main.py
```

или

```
cd bot/
```
```
python3 main.py
```
6. Откройте своего бота и введите команду /start
