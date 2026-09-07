# 🥗 TG Nutritionist (Telegram Bot)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="aiogram">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLModel-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/uv-Package_Manager-DE5B8B?style=for-the-badge&logo=python&logoColor=white" alt="uv">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## 📌 О проекте

**TG Nutritionist** — Практическая работа созданна для упрощения работы нутрициолога, современный и удобный Telegram-бот, разработанный для ведения дневника питания, подсчета калорий и БЖУ, а также трекинга анкетирования и управления подписками.

Бот спроектирован с учетом современных стандартов бэкенд-разработки на Python: использует асинхронный фреймворк **aiogram 3.x**, ORM **SQLModel**, а также встроенную панель администратора на базе **sqladmin** и **FastAPI**.

---

## ✨ Основные возможности

- 📊 **Расчет и трекинг КБЖУ**: Автоматический расчет суточной нормы калорий и БЖУ с учетом целей (похудение, поддержание, набор массы) и уровня активности.
- 📝 **Интерактивное анкетирование**: Сбор метрик пользователя (рост, вес, возраст, цель, уровень активности) в формате удобного диалога.
- 💳 **Система подписок**: Модуль управления доступом и тарифами подписки.
- ⚙️ **Админ-панель (`sqladmin`)**: Удобное управление пользователями, анкетами и рассылками через веб-интерфейс на FastAPI.
- 🐳 **Полная контейнеризация**: Быстрый запуск всей инфраструктуры через Docker и Docker Compose.

---

## 🛠 Технологический стек

- **Язык**: Python 3.11+
- **Пакетный менеджер**: [uv](https://github.com/astral-sh/uv)
- **Telegram Bot Framework**: `aiogram` 3.x
- **Backend / Admin**: `FastAPI`, `sqladmin`
- **База данных & ORM**: `PostgreSQL`, `SQLModel`, `Pydantic v2`
- **Тестирование**: `pytest`
- **Деплой**: `Docker`, `Docker Compose`

---

## 🚀 Быстрый запуск

### 1. Требования

Убедитесь, что у вас установлены:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/)
- [uv](https://github.com/astral-sh/uv) *(если запускаете локально без Docker)*

---

### 2. Клонирование репозитория

```bash

git clone [https://github.com/sobakaww52/tg_nutr.git](https://github.com/sobakaww52/tg_nutr.git)
cd tg_nutr

```
### 3. Настройка окружения

Создайте файл .env на основе примера .env.example:

```bash
cp .env.example .env
```
Заполните переменные окружения в .env:

```Фрагмент кода

# Telegram Bot
BOT_TOKEN=your_telegram_bot_token_here

# Database Settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=tg_nutr
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Admin / Web App
SECRET_KEY=your_super_secret_key_here
```

### 4. Запуск через Docker Compose (Рекомендуется)

```bash
docker compose up -d --build
```

## 📂 Структура проекта
```
tg_nutr/
├── app/
│   ├── admin/          # Настройки и представления sqladmin
│   ├── bot/            # Хэндлеры, мидлвари, клавиатуры aiogram 3.x
│   ├── core/           # Конфигурация, базы данных, сессии
│   ├── models/         # Модели SQLModel / Pydantic v2
│   └── services/       # Бизнес-логика (расчет КБЖУ, подписки)
├── tests/              # Набор автотестов (pytest)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml      # Зависимости и конфигурация uv
└── README.md
```

