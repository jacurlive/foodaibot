from typing import Any
from bot.locales.ru.messages import messages as ru_messages
from bot.locales.en.messages import messages as en_messages
from bot.locales.uz.messages import messages as uz_messages

LOCALES = {
    "ru": ru_messages,
    "en": en_messages,
    "uz": uz_messages,
}

LANGUAGE_NAMES = {
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
    "uz": "🇺🇿 O'zbek",
}

DEFAULT_LANGUAGE = "en"


def get_text(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs: Any) -> str:
    locale = LOCALES.get(lang, LOCALES[DEFAULT_LANGUAGE])
    text = locale.get(key) or LOCALES[DEFAULT_LANGUAGE].get(key, f"[{key}]")
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def t(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs: Any) -> str:
    return get_text(key, lang, **kwargs)
