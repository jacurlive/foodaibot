messages = {
    # --- Common ---
    "btn_back": "◀️ Back",
    "btn_cancel": "❌ Cancel",
    "btn_save": "✅ Save",
    "btn_yes": "✅ Yes",
    "btn_no": "❌ No",
    "btn_skip": "⏭ Skip",
    "error_general": "⚠️ Something went wrong. Please try again later.",
    "error_invalid_input": "❌ Invalid input. Please try again.",
    "error_banned": "🚫 Your account has been banned.",
    "loading": "⏳ Processing...",

    # --- Start / Onboarding ---
    "btn_open_app": "🚀 Open App",
    "welcome_back": (
        "👋 Welcome back!\n\n"
        "Open the app to continue:"
    ),
    "welcome_open_app": (
        "✅ Language selected!\n\n"
        "Open the app to complete setup and start tracking your nutrition:"
    ),
    "welcome": (
        "👋 Hello! I'm <b>FoodAI</b> — your smart nutrition assistant.\n\n"
        "📸 Just send me a photo of your food, and I'll:\n"
        "• Identify the dish\n"
        "• Count calories\n"
        "• Calculate macros (protein, fat, carbs)\n\n"
        "Let's get started! First, select your language:"
    ),
    "onboarding_language_select": "🌍 Select your language:",
    "onboarding_name_ask": (
        "👤 What's your name?\n\n"
        "Enter your name:"
    ),
    "onboarding_age_ask": (
        "🎂 How old are you?\n\n"
        "Enter your age (e.g. <b>25</b>):"
    ),
    "onboarding_age_invalid": "❌ Please enter a valid age (between 10 and 100).",
    "onboarding_gender_ask": "⚧ Select your gender:",
    "btn_gender_male": "👨 Male",
    "btn_gender_female": "👩 Female",
    "onboarding_height_ask": (
        "📏 Enter your height in <b>centimeters</b>:\n"
        "(e.g. <b>175</b>)"
    ),
    "onboarding_height_ask_imperial": (
        "📏 Enter your height in <b>feet.inches</b>:\n"
        "(e.g. <b>5.9</b> for 5'9\")"
    ),
    "onboarding_height_invalid": "❌ Please enter a valid height (100–250 cm).",
    "onboarding_weight_ask": (
        "⚖️ Enter your weight in <b>kilograms</b>:\n"
        "(e.g. <b>70</b>)"
    ),
    "onboarding_weight_ask_imperial": (
        "⚖️ Enter your weight in <b>pounds</b>:\n"
        "(e.g. <b>154</b>)"
    ),
    "onboarding_weight_invalid": "❌ Please enter a valid weight (30–300 kg).",
    "onboarding_goal_ask": "🎯 What is your goal?",
    "btn_goal_lose": "📉 Lose weight",
    "btn_goal_maintain": "⚖️ Maintain weight",
    "btn_goal_gain": "📈 Gain muscle",
    "onboarding_units_ask": "📐 Select your preferred unit system:",
    "btn_units_metric": "🇪🇺 Metric (kg/cm)",
    "btn_units_imperial": "🇺🇸 Imperial (lb/ft)",
    "onboarding_complete": (
        "✅ <b>Profile created!</b>\n\n"
        "👤 Name: <b>{name}</b>\n"
        "🎯 Goal: <b>{goal}</b>\n"
        "🔥 Daily target: <b>{calories} kcal</b>\n\n"
        "Now send me a food photo and I'll analyze it! 📸"
    ),

    # --- Main Menu ---
    "main_menu": "🏠 <b>Main Menu</b>\n\nSend a food photo or choose a section:",
    "btn_diary": "📔 Diary",
    "btn_profile": "👤 Profile",
    "btn_history": "📜 History",
    "btn_settings": "⚙️ Settings",
    "btn_analyze_food": "📸 Analyze Food",

    # --- Food Analysis ---
    "food_send_photo": (
        "📸 Send me a photo of your meal and I'll analyze its nutritional content.\n\n"
        "<i>Best results with good lighting and a clear photo.</i>"
    ),
    "food_analyzing": "🔍 Analyzing photo...",
    "food_not_detected": (
        "❌ <b>Food not detected</b>\n\n"
        "Could not identify a dish in this photo. Please try:\n"
        "• Taking a closer shot\n"
        "• Improving lighting\n"
        "• Making sure there's food in the photo"
    ),
    "food_result": (
        "🍽 <b>{dish_name}</b>\n"
        "⚖️ Portion: <b>~{grams} g</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Calories: <b>{calories} kcal</b>\n"
        "💪 Protein: <b>{protein} g</b>\n"
        "🧈 Fat: <b>{fat} g</b>\n"
        "🍞 Carbs: <b>{carbs} g</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📝 <i>{description}</i>\n\n"
        "✏️ <i>Enter the exact weight of your portion — the bot will recalculate calories and macros automatically.</i>"
    ),
    "food_api_error": (
        "⚠️ <b>Analysis error</b>\n\n"
        "Could not reach the analysis service. Please try again in a moment."
    ),
    "btn_save_entry": "✅ Save",
    "btn_edit_grams": "✏️ Edit grams",
    "btn_discard_entry": "🗑 Don't save",
    "food_ask_grams": "⚖️ Enter the number of grams:",
    "food_grams_invalid": "❌ Please enter a valid number of grams (e.g. <b>150</b>).",
    "food_saved_success": "✅ <b>Saved to diary!</b>",
    "entry_saved": "✅ Entry saved to diary!",
    "entry_discarded": "🗑 Entry not saved.",

    # --- Diary ---
    "diary_title": "📔 <b>Food Diary</b>",
    "btn_diary_today": "📅 Today",
    "btn_diary_week": "📆 This Week",
    "diary_empty": "📭 No entries yet. Send a food photo!",
    "diary_today": (
        "📅 <b>Diary — {date}</b>\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Total: <b>{total_cal} kcal</b>\n"
        "💪 Protein: <b>{total_prot} g</b>  "
        "🧈 Fat: <b>{total_fat} g</b>  "
        "🍞 Carbs: <b>{total_carbs} g</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📊 Remaining: <b>{remaining} kcal</b>"
    ),
    "diary_week": (
        "📆 <b>Diary — This Week</b>\n\n"
        "{entries}\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔥 Total this week: <b>{total_cal} kcal</b>"
    ),
    "diary_entry_line": "• {time} — {dish} ({calories} kcal)\n",
    "diary_day_header": "\n📅 <b>{date}:</b>\n",
    "diary_no_norm": "\n<i>⚠️ Daily calorie target not set. Please complete your profile.</i>",

    # --- Profile ---
    "profile_title": (
        "👤 <b>My Profile</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📛 Name: <b>{name}</b>\n"
        "🎂 Age: <b>{age}</b>\n"
        "⚧ Gender: <b>{gender}</b>\n"
        "📏 Height: <b>{height}</b>\n"
        "⚖️ Weight: <b>{weight}</b>\n"
        "🎯 Goal: <b>{goal}</b>\n"
        "🔥 Daily target: <b>{calories} kcal/day</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "btn_edit_name": "📛 Edit name",
    "btn_edit_age": "🎂 Edit age",
    "btn_edit_gender": "⚧ Edit gender",
    "btn_edit_height": "📏 Edit height",
    "btn_edit_weight": "⚖️ Edit weight",
    "btn_edit_goal": "🎯 Edit goal",
    "btn_recalc_calories": "🔄 Recalculate target",
    "profile_updated": "✅ Profile updated!",
    "calories_recalculated": "🔥 Daily calorie target recalculated: <b>{calories} kcal/day</b>",
    "gender_male": "Male",
    "gender_female": "Female",
    "goal_lose": "Lose weight",
    "goal_maintain": "Maintain weight",
    "goal_gain": "Gain muscle",

    # --- History ---
    "history_title": "📜 <b>Analysis History</b>",
    "history_empty": "📭 History is empty. Start analyzing your meals!",
    "history_entry": (
        "🍽 <b>{dish}</b>\n"
        "📅 {date}  🔥 {calories} kcal\n"
        "💪 P: {protein}g  🧈 F: {fat}g  🍞 C: {carbs}g"
    ),
    "btn_delete_entry": "🗑 Delete",
    "entry_deleted": "✅ Entry deleted.",
    "btn_prev_page": "◀️",
    "btn_next_page": "▶️",
    "history_page": "Page {page}/{total}",

    # --- Settings ---
    "settings_title": "⚙️ <b>Settings</b>",
    "btn_change_language": "🌍 Language",
    "btn_change_units": "📐 Units",
    "btn_notifications": "🔔 Notifications",
    "settings_language": "🌍 <b>Language Selection</b>\n\nCurrent language: <b>English</b>",
    "settings_units": "📐 <b>Units</b>\n\nCurrent system: <b>{units}</b>",
    "units_metric": "Metric (kg/cm)",
    "units_imperial": "Imperial (lb/ft)",
    "settings_units_changed": "✅ Units changed to <b>{units}</b>.",
    "settings_language_changed": "✅ Language changed!",
    "notifications_title": (
        "🔔 <b>Notifications</b>\n\n"
        "Set meal reminders:"
    ),
    "btn_notify_morning": "🌅 Morning (8:00)",
    "btn_notify_afternoon": "☀️ Lunch (13:00)",
    "btn_notify_evening": "🌙 Dinner (19:00)",
    "notify_on": "✅ On",
    "notify_off": "🔕 Off",
    "notify_updated": "✅ Notification settings updated!",

    # --- Admin ---
    "admin_panel": (
        "👑 <b>Admin Panel</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👥 Total users: <b>{total_users}</b>\n"
        "🆕 Today: <b>{today}</b>\n"
        "📅 This week: <b>{week}</b>\n"
        "📆 This month: <b>{month}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📸 Total analyses: <b>{total_analyses}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    ),
    "btn_admin_broadcast": "📢 Broadcast",
    "btn_admin_top_users": "🏆 Top Users",
    "btn_admin_ban": "🚫 Ban/Unban",
    "admin_broadcast_ask": "📢 Enter the message to broadcast to all users:",
    "admin_broadcast_confirm": "Send broadcast to <b>{count}</b> users?\n\n{text}",
    "admin_broadcast_done": "✅ Broadcast sent to <b>{sent}</b> users.",
    "admin_top_users": "🏆 <b>Most Active Users</b>\n\n{users}",
    "admin_top_user_line": "{rank}. {name} — {count} analyses\n",
    "admin_ban_ask": "🚫 Enter the Telegram ID of the user to ban/unban:",
    "admin_ban_done": "🚫 User <b>{user_id}</b> has been banned.",
    "admin_unban_done": "✅ User <b>{user_id}</b> has been unbanned.",
    "admin_user_not_found": "❌ User not found.",
    "not_admin": "❌ You don't have admin privileges.",
}
