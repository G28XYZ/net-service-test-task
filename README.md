# Junior Fullstack Test Task

Тестовое задание представляет собой мини-сервис управления виртуальной инфраструктурой:

- авторизация пользователя;
- просмотр списка виртуальных машин;
- просмотр списка сетей и интерфейсов;
- создание виртуальной машины;
- создание сетевого интерфейса;
- заготовленные API-обработчики и UI для включения/выключения ВМ и интерфейса.

## Стек

- Backend: FastAPI
- Database: PostgreSQL, в проекте есть заготовка подключения в [backend/app/database/main.py](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/database/main.py:1)
- Frontend: React + Vite

## Что уже реализовано

- логин по демо-учетке `admin` / `admin`;
- токен-авторизация через `Bearer`;
- сохранение сетей, ВМ и интерфейсов в PostgreSQL;
- автоматическое создание таблиц и сидирование демо-данных при старте backend;
- модели `VirtualMachine`, `NetworkInterface`, `Network` с базовыми полями `id`, `name`, `status`, `createdAt`;
- создание ВМ;
- создание интерфейса с привязкой к ВМ и сети;
- React-интерфейс для входа, просмотра и создания сущностей;
- кнопки для смены статуса ВМ и интерфейса.

## Что нужно сделать кандидату

Нужно реализовать два обработчика:

1. Включение и выключение виртуальной машины.
2. Включение и выключение сетевого интерфейса.

Точки входа:

- [backend/app/api/routes/virtual_machines.py](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/api/routes/virtual_machines.py:51)
- [backend/app/api/routes/interfaces.py](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/api/routes/interfaces.py:65)

Сейчас эти методы возвращают `501 Not Implemented`.

## Ожидаемое поведение

- Для ВМ допустимы переходы `running -> stopped` и `stopped -> running`.
- Для интерфейса допустимы переходы `up -> down` и `down -> up`.
- Если сущность не найдена, нужно вернуть `404`.
- Если передан недопустимый статус, нужно вернуть `400`.
- После успешного изменения должен вернуться обновленный объект.

Можно расширить логику валидации, если кандидат сочтет это нужным.

## Запуск backend

```bash
make backend-install
make backend-run
```

Проверка подключения к PostgreSQL:

```bash
make backend-db-check
```

## Запуск frontend

```bash
make frontend-install
make frontend-run
```

Frontend поднимается на `http://localhost:5173`, backend ожидается на `http://127.0.0.1:8000`.

После первого запуска backend автоматически создаст таблицы в PostgreSQL и заполнит их начальными данными.

## Быстрый старт

```bash
make install
make dev
```

`make dev` запускает backend и frontend одновременно.

## Как проверять

- Войти под `admin` / `admin`
- Создать новую ВМ
- Создать новый интерфейс
- Переключить `ON/OFF` для ВМ
- Переключить `ON/OFF` для интерфейса
- Убедиться, что после реализации обработчиков статус действительно меняется в ответе API и на UI

## Структура

- [backend/app/main.py](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/main.py:1) - инициализация FastAPI
- [backend/app/api/routes](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/api/routes) - роуты
- [backend/app/database](/Users/royalfly/Documents/GitHub/net-service-test-task/backend/app/database) - подключение к БД, сессии и инициализация схемы
- [frontend/src/App.jsx](/Users/royalfly/Documents/GitHub/net-service-test-task/frontend/src/App.jsx:1) - основной экран
- [frontend/src/api/client.js](/Users/royalfly/Documents/GitHub/net-service-test-task/frontend/src/api/client.js:1) - запросы к backend
