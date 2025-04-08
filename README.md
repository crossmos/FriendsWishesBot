# FriednsWishesBot
## Как запустить проект
1. Создать бот через @BotFather и получить токен этого бота
2. Переименовать файл ".env-template" в ".env" и вставить туда свой токен
3. Установить и запустить вирутальное окружение

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
