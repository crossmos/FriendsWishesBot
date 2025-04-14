DOCKER_STATUS = True

if DOCKER_STATUS:
    TELEGRAM_USERS_URL = 'http://api-backend:8000/api/v1/telegram_users/'
    WISHES_URL = 'http://api-backend:8000/api/v1/wishes/'
else:
    TELEGRAM_USERS_URL = 'http://127.0.0.1:8000/api/v1/telegram_users/'
    WISHES_URL = 'http://127.0.0.1:8000/api/v1/wishes/'
