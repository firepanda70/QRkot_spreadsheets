# QRkot - Фонд помощи котам

Фонд собирает пожертвования на различные благотвоительные проекты для помощи котикам.

## Использование

Суперпользователь создает благотворительные проекты, определяет
необходимую дл него сумму, добавляет оисанеие. Польователи, после аутентификации и авторизации, переводят в фонд пожертвования. Пожертвования начисляются в копилку проектов в порядке их открыия. 

### Установка
- Скачать проект:
```
git clone https://github.com/firepanda70/QRkot_spreadsheets
```
- Перейти в директорию с проектом:
```
cd cat_charity_fund/
```
- Создать виртуальное окружение:
```
python3 -m venv venv
```
- Активировать виртуальное окружение:
```
. venv/bin/activate
```
- Установить зависимости:
```
pip install -r requirements.txt
```
- Создать файл `.env` с настройками:
```
APP_TITLE=<Ваше название приложения>
DESCRIPTION=<Ваше описание проекта>
DATABASE_URL=<Настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
EMAIL=<Адрес сервисного аккаунта Google>
# Начало данных сервистного аккаунта Google Cloud Platform
TYPE=service_account
PROJECT_ID=project-id
PRIVATE_KEY_ID=private-key-id
CLIENT_EMAIL=client-email
CLIENT_ID=client-id
AUTH_URI=auth-uri
TOKE_URI=token-uri
AUTH_PROVIDER_X509_CERT_URL=provider-cert-url
CLIENT_X509_CERT_URL=client-cert-url
# Конец данных сервистного аккаунта Google Cloud Platform
```
- Применить миграции для создания БД:
```
alembic upgrade head
```
- Запустить приложение:
```
uvicorn app.main:app 
```
Документация API будет доступна по адресу:
```
http://127.0.0.1:8000/docs
```

## Технологии
- Python 3.9
- FastAPI
- SQLAlchemy
- Google API