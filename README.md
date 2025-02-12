API для реферальной системы

Стэк: FastAPI, SQLAlchemy, SQLite, Docker

1) Сперва необходимо создать и настроить .env файл:

SECRET_KEY=YOUR_SECRET_KEY

ALGORITHM=CHOOSE_ALGORITHM (Например, HS256, RS256, ES256)

2) Собираем образ:
docker build -t referral-image .

Для первого запуска:
docker run -d -p 8000:80 --name referral-container referral-image

Остановить контейнер можно командой:
docker stop referral-container

Для последующих запусков контейнера:
docker start referral-container