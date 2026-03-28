# 🍽 FoodAI — Telegram Bot

Умный Telegram-бот для анализа питания с использованием ИИ.
Отправьте фото еды — бот определит блюдо, подсчитает калории и рассчитает БЖУ.

## Возможности

- 📸 **Анализ фото** — определение блюда, калорий, белков, жиров, углеводов через GPT-4o
- 📔 **Дневник питания** — автоматическое сохранение, просмотр по дням и неделям
- 👤 **Профиль** — возраст, пол, рост, вес, цель; норма калорий по формуле Миффлина-Сан Жеора
- 🌍 **Мультиязычность** — русский, английский, узбекский
- ⚙️ **Настройки** — язык, единицы измерения (метрика/имперская), уведомления
- 👑 **Админ-панель** — статистика, рассылка, бан/разбан пользователей

---

## Быстрый старт (Docker)

### 1. Клонируйте репозиторий и настройте окружение

```bash
cp .env.example .env
```

Заполните `.env`:

```env
BOT_TOKEN=ваш_токен_от_BotFather
OPENAI_API_KEY=ваш_openai_ключ
ADMIN_IDS=ваш_telegram_id
```

### 2. Запустите через Docker Compose

```bash
docker-compose up -d --build
```

Бот автоматически применит миграции и запустится.

### 3. Проверьте логи

```bash
docker-compose logs -f bot
```

---

## Ручная установка (без Docker)

### Требования

- Python 3.11+
- PostgreSQL 14+

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Настройте `.env`

```env
BOT_TOKEN=...
OPENAI_API_KEY=...
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/foodai_db
ADMIN_IDS=123456789
```

### 3. Примените миграции

```bash
alembic upgrade head
```

### 4. Запустите бота

```bash
python -m bot.main
```

---

## Структура проекта

```
foodaibot/
├── bot/
│   ├── main.py              # Точка входа
│   ├── config.py            # Конфигурация (pydantic-settings)
│   ├── database.py          # Движок SQLAlchemy
│   ├── handlers/            # Обработчики сообщений и callback'ов
│   │   ├── start.py         # /start, главное меню
│   │   ├── onboarding.py    # FSM онбординга
│   │   ├── food.py          # Анализ фото еды
│   │   ├── profile.py       # Просмотр/редактирование профиля
│   │   ├── diary.py         # Дневник питания
│   │   ├── history.py       # История с пагинацией
│   │   ├── settings.py      # Язык, единицы, уведомления
│   │   └── admin.py         # Панель администратора
│   ├── keyboards/           # Inline-клавиатуры
│   ├── services/            # Бизнес-логика
│   │   ├── openai_service.py  # GPT-4o vision API
│   │   ├── user_service.py    # CRUD пользователей
│   │   ├── diary_service.py   # CRUD записей дневника
│   │   └── admin_service.py   # Статистика и бан
│   ├── models/              # SQLAlchemy модели
│   │   ├── user.py
│   │   └── food_entry.py
│   ├── middlewares/
│   │   ├── db.py            # Сессия БД на каждый запрос
│   │   └── user.py          # Получение/создание пользователя
│   └── locales/             # Переводы (ru/en/uz)
├── migrations/              # Alembic миграции
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Переменные окружения

| Переменная | Описание | Обязательно |
|---|---|---|
| `BOT_TOKEN` | Токен Telegram бота (от @BotFather) | ✅ |
| `OPENAI_API_KEY` | Ключ OpenAI API | ✅ |
| `DATABASE_URL` | URL PostgreSQL | ✅ |
| `ADMIN_IDS` | Telegram ID администраторов через запятую | — |
| `OPENAI_MODEL` | Модель OpenAI (по умолчанию `gpt-4o`) | — |
| `LOG_LEVEL` | Уровень логирования (INFO/DEBUG) | — |

---

## Команды бота

| Команда | Описание |
|---|---|
| `/start` | Запуск / главное меню |
| `/admin` | Панель администратора (только для admins) |

---

## Формула расчёта калорий

Используется формула **Миффлина — Сан Жеора** с умеренной активностью (×1.55):

- **Мужчины**: BMR = 10×вес + 6.25×рост − 5×возраст + 5
- **Женщины**: BMR = 10×вес + 6.25×рост − 5×возраст − 161

Цели:
- 📉 Похудеть: TDEE − 500 ккал
- ⚖️ Поддержать: TDEE
- 📈 Набрать: TDEE + 300 ккал
