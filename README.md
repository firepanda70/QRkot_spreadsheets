# QRkot - Фонд помощи котам

Фонд собирает пожертвования на различные благотвоительные проекты для помощи котикам. 

## Использовано
- Python 3.9
- FastAPI
- SQLAlchemy
- Google API

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