# Проект "QRKot" Благотворительного фонда поддержки котиков

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.  
*Проект реализован самостоятельно на курсе от Я.Практикум "Python-разработчик расширенный".*


## Установка и быстрый запуск:  

1. Клонируйте репозиторий:  

    ```bash
    git clone https://github.com/yourusername/cat_charity_fund.git
    ```  

2. Установите зависимости:  

    ```bash
    pip install -r requirements.txt
    ```  

3. Выполнить миграцию для создания БД(если нет) и таблиц:  

    ```bash
    alembic upgrade head
    ```  

4. Задайте в директории `/cat_charity_fund` создайте файл `.env` и укажите следующие следующие переменные:  

- DATABASE_URL=sqlite+aiosqlite:///./qrcat.db - подключение к БД(sqlite)  
- SECRET=Ваш секретный код для FastAPi User  
- FIRST_SUPERUSER_EMAIL=admin@qrcot.meow - создание суперпользователя при первом запуске  
- FIRST_SUPERUSER_PASSWORD=meowmeow - пароль для суперадмина  

5. Запустите проект из директории */cat_charity_fund*:  

    ```bash
    uvicorn app.main:app
    ```  

## Эндпоинты  

Все эндопинты и документацию по API можно посмотреть после запуска проекта по ссылкам:  
Swagger: **http://<your_url>/docs**  
ReDoc: **http://<your_url>/docs**  
Для ознакомления без запуска можно загрузить файл `/cat_charity_fund/openapi.py` на сайт [ReDoc interactive demo](https://redocly.github.io/redoc/)


## Дополнительные параметры  

В `/cat_charity_fund/app/core/config.py` можно задать дополнительные параметры для проекта, например:  
- DEFAULT_AMOUNT = 0 - начальное значение инвестиций в проект;  
- GT_FOR_AMOUNT = 0 - значение больше которого можно задонатить и сколько требуется проекту донатов;  
- MAX_LENGTH_NAME = 100 - максимальная длина имени проекта;  
- MIN_LENGTH_NAME = 1 - минимальная длина имени проекта;  
- MIN_LENGTH_DESCRIPTION = 1 - минимальная длина описания проекта;  


## Запуск тестов  

    ```bash
    pytest
    ```  
Также присутствует коллекция тестов для PostMan, перед выполнением необходимо запустить скрипт:  
    ```bash
    python3 setup_for_postman
    ```  

## Фреймворки и основные библиотеки используемые в проекте:  

FastAPI v0.78.0  
fastapi-users v10.0.4  
alembic v 1.7.7  
pydantic v1.10.0  
SQLAlchemy v1.4.36  


## Автор  

Автор проекта: [Даниил](https://github.com/Danuuuq)  
Связаться через [Telegram](https://t.me/saint_danik)  | [Email](mailto:daniil@tyunkov.ru)
