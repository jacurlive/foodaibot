from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.locales import t
from bot.models.food_entry import FoodEntry


def history_keyboard(
    entries: list[FoodEntry],
    lang: str,
    page: int,
    total_pages: int,
) -> InlineKeyboardMarkup:
    buttons = []

    # Delete buttons for each entry
    for entry in entries:
        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {entry.dish_name[:30]}",
                callback_data=f"history:delete:{entry.id}",
            )
        ])

    # Pagination
    nav_row = []
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(text=t("btn_prev_page", lang), callback_data=f"history:page:{page - 1}")
        )
    if page < total_pages:
        nav_row.append(
            InlineKeyboardButton(text=t("btn_next_page", lang), callback_data=f"history:page:{page + 1}")
        )
    if nav_row:
        buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
