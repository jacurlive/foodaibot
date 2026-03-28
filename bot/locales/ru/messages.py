messages = {
    # --- Common ---
    "btn_back": "◀️ Назад",
    "btn_cancel": "❌ Отмена",
    "btn_save": "✅ Сохранить",
    "btn_yes": "✅ Да",
    "btn_no": "❌ Нет",
    "btn_skip": "⏭ Пропустить",
    "error_general": "⚠️ Что-то пошло не так. Попробуйте позже.",
    "error_invalid_input": "❌ Некорректный ввод. Попробуйте снова.",
    "error_banned": "🚫 Ваш аккаунт заблокирован.",
    "loading": "⏳ Обрабатываю...",

    # --- Start / Onboarding ---
    "btn_open_app": "🚀 Открыть приложение",
    "welcome_back": (
        "👋 С возвращением!\n\n"
        "Откройте приложение, чтобы продолжить:"
    ),
    "welcome_open_app": (
        "✅ Язык выбран!\n\n"
        "Откройте приложение, чтобы завершить настройку и начать отслеживать питание:"
    ),
    "welcome": (
        "👋 Привет! Я <b>FoodAI</b> — ваш умный помощник по питанию.\n\n"
        "📸 Просто отправьте мне фото еды, и я:\n"
        "• Определю блюдо\n"
        "• Подсчитаю калории\n"
        "• Рассчитаю БЖУ\n\n"
        "Давайте начнём! Сначала выберите язык:"
    ),
    "onboarding_language_select": "🌍 Выберите язык интерфейса:",
    "onboarding_name_ask": (
        "👤 Как вас зовут?\n\n"
        "Введите ваше имя:"
    ),
    "onboarding_age_ask": (
        "🎂 Сколько вам лет?\n\n"
        "Введите возраст (например: <b>25</b>):"
    ),
    "onboarding_age_invalid": "❌ Введите корректный возраст (от 10 до 100 лет).",
    "onboarding_gender_ask": "⚧ Выберите пол:",
    "btn_gender_male": "👨 Мужской",
    "btn_gender_female": "👩 Женский",
    "onboarding_height_ask": (
        "📏 Введите ваш рост в <b>сантиметрах</b>:\n"
        "(например: <b>175</b>)"
    ),
    "onboarding_height_ask_imperial": (
        "📏 Введите ваш рост в <b>футах и дюймах</b>:\n"
        "(например: <b>5.9</b> для 5'9\")"
    ),
    "onboarding_height_invalid": "❌ Введите корректный рост (от 100 до 250 см).",
    "onboarding_weight_ask": (
        "⚖️ Введите ваш вес в <b>килограммах</b>:\n"
        "(например: <b>70</b>)"
    ),
    "onboarding_weight_ask_imperial": (
        "⚖️ Введите ваш вес в <b>фунтах</b>:\n"
        "(например: <b>154</b>)"
    ),
    "onboarding_weight_invalid": "❌ Введите корректный вес (от 30 до 300 кг).",
    "onboarding_goal_ask": "🎯 Какова ваша цель?",
    "btn_goal_lose": "📉 Похудеть",
    "btn_goal_maintain": "⚖️ Поддержать вес",
    "btn_goal_gain": "📈 Набрать массу",
    "onboarding_units_ask": "📐 Выберите систему единиц:",
    "btn_units_metric": "🇪🇺 Метрическая (кг/см)",
    "btn_units_imperial": "🇺🇸 Имперская (lb/ft)",
    "onboarding_complete": (
        "✅ <b>Профиль создан!</b>\n\n"
        "👤 Имя: <b>{name}</b>\n"
        "🎯 Цель: <b>{goal}</b>\n"
        "🔥 Дневная норма: <b>{calories} ккал</b>\n\n"
        "Теперь отправьте мне фото еды, и я всё проанализирую! 📸"
    ),

    # --- Main Menu ---
    "main_menu": "🏠 <b>Главное меню</b>\n\nОтправьте фото еды или выберите раздел:",
    "btn_diary": "📔 Дневник",
    "btn_profile": "👤 Профиль",
    "btn_history": "📜 История",
    "btn_settings": "⚙️ Настройки",
    "btn_analyze_food": "📸 Анализ еды",

    # --- Food Analysis ---
    "food_send_photo": (
        "📸 Отправьте фото блюда, и я проанализирую его состав и калорийность.\n\n"
        "<i>Лучшие результаты при хорошем освещении и чётком фото.</i>"
    ),
    "food_analyzing": "🔍 Анализирую фото...",
    "food_not_detected": (
        "❌ <b>Еда не обнаружена</b>\n\n"
        "На фото не удалось определить блюдо. Попробуйте:\n"
        "• Сфотографировать крупнее\n"
        "• Улучшить освещение\n"
        "• Убедиться, что на фото еда"
    ),
    "food_result": (
        "🍽 <b>{dish_name}</b>\n"
        "⚖️ Порция: <b>~{grams} г</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Калории: <b>{calories} ккал</b>\n"
        "💪 Белки: <b>{protein} г</b>\n"
        "🧈 Жиры: <b>{fat} г</b>\n"
        "🍞 Углеводы: <b>{carbs} г</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📝 <i>{description}</i>\n\n"
        "✏️ <i>Укажите точный вес порции — бот пересчитает калории и БЖУ автоматически.</i>"
    ),
    "food_api_error": (
        "⚠️ <b>Ошибка анализа</b>\n\n"
        "Не удалось связаться с сервисом. Попробуйте через минуту."
    ),
    "btn_save_entry": "✅ Сохранить",
    "btn_edit_grams": "✏️ Изменить граммы",
    "btn_discard_entry": "🗑 Не сохранять",
    "food_ask_grams": "⚖️ Введите количество граммов:",
    "food_grams_invalid": "❌ Введите корректное число граммов (например: <b>150</b>).",
    "food_saved_success": "✅ <b>Сохранено в дневник!</b>",
    "entry_saved": "✅ Запись сохранена в дневник!",
    "entry_discarded": "🗑 Запись не сохранена.",

    # --- Diary ---
    "diary_title": "📔 <b>Дневник питания</b>",
    "btn_diary_today": "📅 Сегодня",
    "btn_diary_week": "📆 Неделя",
    "diary_empty": "📭 Записей пока нет. Отправьте фото еды!",
    "diary_today": (
        "📅 <b>Дневник — {date}</b>\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Итого: <b>{total_cal} ккал</b>\n"
        "💪 Белки: <b>{total_prot} г</b>  "
        "🧈 Жиры: <b>{total_fat} г</b>  "
        "🍞 Углеводы: <b>{total_carbs} г</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📊 Осталось: <b>{remaining} ккал</b>"
    ),
    "diary_week": (
        "📆 <b>Дневник — неделя</b>\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Всего за неделю: <b>{total_cal} ккал</b>"
    ),
    "diary_entry_line": "• {time} — {dish} ({calories} ккал)\n",
    "diary_day_header": "\n📅 <b>{date}:</b>\n",
    "diary_no_norm": "\n<i>⚠️ Норма калорий не задана. Заполните профиль.</i>",

    # --- Profile ---
    "profile_title": (
        "👤 <b>Мой профиль</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📛 Имя: <b>{name}</b>\n"
        "🎂 Возраст: <b>{age}</b>\n"
        "⚧ Пол: <b>{gender}</b>\n"
        "📏 Рост: <b>{height}</b>\n"
        "⚖️ Вес: <b>{weight}</b>\n"
        "🎯 Цель: <b>{goal}</b>\n"
        "🔥 Норма: <b>{calories} ккал/день</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "btn_edit_name": "📛 Изменить имя",
    "btn_edit_age": "🎂 Изменить возраст",
    "btn_edit_gender": "⚧ Изменить пол",
    "btn_edit_height": "📏 Изменить рост",
    "btn_edit_weight": "⚖️ Изменить вес",
    "btn_edit_goal": "🎯 Изменить цель",
    "btn_recalc_calories": "🔄 Пересчитать норму",
    "profile_updated": "✅ Профиль обновлён!",
    "calories_recalculated": "🔥 Норма калорий пересчитана: <b>{calories} ккал/день</b>",
    "gender_male": "Мужской",
    "gender_female": "Женский",
    "goal_lose": "Похудеть",
    "goal_maintain": "Поддержать вес",
    "goal_gain": "Набрать массу",

    # --- History ---
    "history_title": "📜 <b>История анализов</b>",
    "history_empty": "📭 История пуста. Начните анализировать блюда!",
    "history_entry": (
        "🍽 <b>{dish}</b>\n"
        "📅 {date}  🔥 {calories} ккал\n"
        "💪 Б: {protein}г  🧈 Ж: {fat}г  🍞 У: {carbs}г"
    ),
    "btn_delete_entry": "🗑 Удалить",
    "entry_deleted": "✅ Запись удалена.",
    "btn_prev_page": "◀️",
    "btn_next_page": "▶️",
    "history_page": "Страница {page}/{total}",

    # --- Settings ---
    "settings_title": "⚙️ <b>Настройки</b>",
    "btn_change_language": "🌍 Язык",
    "btn_change_units": "📐 Единицы измерения",
    "btn_notifications": "🔔 Уведомления",
    "settings_language": "🌍 <b>Выбор языка</b>\n\nТекущий язык: <b>Русский</b>",
    "settings_units": "📐 <b>Единицы измерения</b>\n\nТекущая система: <b>{units}</b>",
    "units_metric": "Метрическая (кг/см)",
    "units_imperial": "Имперская (lb/ft)",
    "settings_units_changed": "✅ Система единиц изменена на <b>{units}</b>.",
    "settings_language_changed": "✅ Язык изменён!",
    "notifications_title": (
        "🔔 <b>Уведомления</b>\n\n"
        "Настройте напоминания о приёмах пищи:"
    ),
    "btn_notify_morning": "🌅 Утро (8:00)",
    "btn_notify_afternoon": "☀️ Обед (13:00)",
    "btn_notify_evening": "🌙 Ужин (19:00)",
    "notify_on": "✅ Вкл",
    "notify_off": "🔕 Выкл",
    "notify_updated": "✅ Настройки уведомлений обновлены!",

    # --- Admin ---
    "admin_panel": (
        "👑 <b>Панель администратора</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👥 Всего пользователей: <b>{total_users}</b>\n"
        "🆕 Сегодня: <b>{today}</b>\n"
        "📅 За неделю: <b>{week}</b>\n"
        "📆 За месяц: <b>{month}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Всего анализов: <b>{total_analyses}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "btn_admin_broadcast": "📢 Рассылка",
    "btn_admin_top_users": "🏆 Топ пользователей",
    "btn_admin_ban": "🚫 Бан/Разбан",
    "admin_broadcast_ask": "📢 Введите текст сообщения для рассылки всем пользователям:",
    "admin_broadcast_confirm": "Отправить рассылку <b>{count}</b> пользователям?\n\n{text}",
    "admin_broadcast_done": "✅ Рассылка отправлена <b>{sent}</b> пользователям.",
    "admin_top_users": "🏆 <b>Самые активные пользователи</b>\n\n{users}",
    "admin_top_user_line": "{rank}. {name} — {count} анализов\n",
    "admin_ban_ask": "🚫 Введите Telegram ID пользователя для бана/разбана:",
    "admin_ban_done": "🚫 Пользователь <b>{user_id}</b> заблокирован.",
    "admin_unban_done": "✅ Пользователь <b>{user_id}</b> разблокирован.",
    "admin_user_not_found": "❌ Пользователь не найден.",
    "not_admin": "❌ У вас нет прав администратора.",
}
