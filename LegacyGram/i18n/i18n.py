from hook_utils import find_class

from LegacyGram.i18n.locales import STRINGS


def get_system_language() -> str:
    try:
        Locale = find_class("java.util.Locale")
        lang = Locale.getDefault().getLanguage()
        if lang in STRINGS:
            return lang
    except Exception:
        pass

    return "en"


def t(key: str, *args) -> str:
    """Translates and replaces {0}, {1} placeholders with provided arguments"""
    lang = get_system_language()
    target_locale = STRINGS.get(lang, STRINGS.get("en", {}))
    result = target_locale.get(key)
    if result is None:
        return f"MISSING: {key}"

    return result.format(*args)
