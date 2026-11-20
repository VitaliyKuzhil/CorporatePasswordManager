# CorporatePasswordManager

**Corporate Password Manager** — це захищена внутрішня корпоративна система для централізованого зберігання, управління та обміну корпоративними паролями. Система дозволяє адміністраторам гнучко контролювати доступ до облікових даних сервісів, а співробітникам — швидко та безпечно знаходити потрібні доступи.

## Стек технологій

- **Frontend:** Vue 3 (Composition API), TypeScript, Vue Router, Pinia, Vite.
- **Backend:** FastAPI (Python 3.11), SQLAlchemy 2.0 (Async), Pydantic.
- **Database:** MySQL 8.4 (асинхронний драйвер `asyncmy`).
- **Infrastructure:** Docker, Docker Compose, phpMyAdmin (для управління БД).
- **Security:** JWT-авторизація, двостороннє AES-шифрування паролів (через `cryptography/Fernet`), CORS.

## Вимоги до середовища

Для запуску проєкту на вашому комп'ютері або сервері повинні бути встановлені:
- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Локальне розгортання

**1. Клонуйте репозиторій:**
```bash
git clone https://github.com/VitaliyKuzhil/CorporatePasswordManager.git
```
```bash
cd CorporatePasswordManager
```

**2. Налаштуйте змінні середовища:**
Проєкт містить файл-приклад конфігурації .env.example. Скопіюйте його, створіть робочий файл .env та заповніть своїми даними:
```bash 
cp .env.example .env
```

**3. Зберіть та запустіть контейнери:**
Під час першого запуску Docker завантажить необхідні образи, встановить залежності Python та Node.js, а також ініціалізує базу даних і створить обліковий запис адміністратора за замовчуванням.
```bash
docker compose up -d --build
```

## Доступ до сервісів
Після успішного запуску сервіси будуть доступні за такими адресами:

Frontend (Vue 3 UI): http://localhost:5173

Frontend DevTools: http://localhost:5173/devtools/

Backend API: http://localhost:8001

API Documentation (Swagger): http://localhost:8001/docs

phpMyAdmin (Управління БД): http://localhost:8081

## Корисні команди Docker
Зупинити проєкт:
```bash
docker compose stop
```

Зупинити та видалити контейнери:
```bash
docker compose down
```

Переглянути логи всіх сервісів:
```bash
docker compose logs -f
```

Перебудувати проєкт після оновлення конфігурації або залежностей:
```bash
docker compose up -d --build
```
