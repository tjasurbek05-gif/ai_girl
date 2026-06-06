from typing import Any

STRINGS: dict[str, dict[str, Any]] = {
    "en": {
        # Onboarding
        "choose_lang": "👋 Welcome to <b>Velvet</b>!\n\nChoose your language:",
        "lang_set": "Language set ✅",

        # Main menu
        "main_menu": (
            "🏠 <b>Main Menu</b>\n\n"
            "⚡ Energy: <b>{energy}/49</b>  |  💎 Gems: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Premium: <b>active</b> until {expires}",
        "sub_none": "✨ Premium: <b>not active</b>",

        # Characters
        "choose_character": (
            "💬 <b>Choose a character</b>\n"
            "Who would you like to spend time with?"
        ),
        "character_card": (
            "{avatar} <b>{name}</b>\n"
            "<i>{tagline}</i>\n\n"
            "🎭 <b>Choose a scenario:</b>"
        ),
        "not_enough_gems": (
            "💎 <b>Not enough gems!</b>\n\n"
            "This scenario costs <b>{cost} gems</b>.\n"
            "You have <b>{gems}</b>.\n\n"
            "Visit the 🛍️ Shop to get more."
        ),
        "gems_spent": "💎 <b>{cost} gems</b> spent. Let's begin! ✨",

        # Chat
        "chat_new": "✨ <i>Starting a new conversation…</i>",
        "chat_continue": "✨ <i>Continuing your conversation…</i>",
        "chat_reset_done": "🔄 <i>Chat cleared. Starting fresh…</i>",
        "no_energy": (
            "⚡ <b>Out of energy!</b>\n\n"
            "Your energy resets every day at midnight.\n\n"
            "Get <b>Premium</b> for unlimited messages! ✨"
        ),
        "ai_error": "⚠️ Couldn't get a response. Please try again.",
        "chat_hint": "<i>Type your message to {name}…</i>",

        # Profile
        "profile": (
            "👤 <b>Your Profile</b>\n\n"
            "⚡ Energy today: <b>{energy}/49</b>\n"
            "💎 Gems: <b>{gems}</b>\n"
            "✨ Premium: {sub_status}\n"
            "📅 Member since: <code>{created_at}</code>"
        ),
        "premium_until": "active until <b>{expires}</b>",
        "no_premium": "not active",

        # Shop
        "shop_title": (
            "🛍️ <b>Shop</b>\n\n"
            "Upgrade to <b>Premium</b>:\n"
            "• ⚡ Unlimited daily energy\n"
            "• 💎 Gems to unlock special scenarios\n\n"
            "Paid securely with ⭐ Telegram Stars."
        ),
        "invoice_title": "Velvet Premium — {label}",
        "invoice_desc": "Unlimited energy for {label} + {gems} 💎 gems",
        "payment_ok": (
            "✅ <b>Payment received — thank you!</b>\n\n"
            "⭐ Premium active until <b>{expires}</b>\n"
            "💎 <b>+{gems} gems</b> added to your account!"
        ),

        # Generic
        "back": "← Back",
        "main_menu_btn": "🏠 Main Menu",
        "reset_chat": "🔄 Reset chat",
        "error_generic": "⚠️ Something went wrong. Please try again.",
    },

    "ru": {
        # Onboarding
        "choose_lang": "👋 Добро пожаловать в <b>Velvet</b>!\n\nВыбери язык:",
        "lang_set": "Язык установлен ✅",

        # Main menu
        "main_menu": (
            "🏠 <b>Главное меню</b>\n\n"
            "⚡ Энергия: <b>{energy}/49</b>  |  💎 Кристаллы: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Премиум: <b>активен</b> до {expires}",
        "sub_none": "✨ Премиум: <b>не активен</b>",

        # Characters
        "choose_character": (
            "💬 <b>Выбери персонажа</b>\n"
            "С кем хочешь провести время?"
        ),
        "character_card": (
            "{avatar} <b>{name}</b>\n"
            "<i>{tagline}</i>\n\n"
            "🎭 <b>Выбери сценарий:</b>"
        ),
        "not_enough_gems": (
            "💎 <b>Недостаточно кристаллов!</b>\n\n"
            "Этот сценарий стоит <b>{cost} кристаллов</b>.\n"
            "У тебя <b>{gems}</b>.\n\n"
            "Зайди в 🛍️ Магазин, чтобы получить больше."
        ),
        "gems_spent": "💎 Потрачено <b>{cost} кристаллов</b>. Начинаем! ✨",

        # Chat
        "chat_new": "✨ <i>Начинаем новый разговор…</i>",
        "chat_continue": "✨ <i>Продолжаем разговор…</i>",
        "chat_reset_done": "🔄 <i>Чат очищен. Начинаем сначала…</i>",
        "no_energy": (
            "⚡ <b>Энергия закончилась!</b>\n\n"
            "Энергия обновляется каждую ночь в полночь.\n\n"
            "Получи <b>Премиум</b> для безлимитных сообщений! ✨"
        ),
        "ai_error": "⚠️ Не удалось получить ответ. Попробуй ещё раз.",
        "chat_hint": "<i>Напиши сообщение для {name}…</i>",

        # Profile
        "profile": (
            "👤 <b>Твой профиль</b>\n\n"
            "⚡ Энергия сегодня: <b>{energy}/49</b>\n"
            "💎 Кристаллы: <b>{gems}</b>\n"
            "✨ Премиум: {sub_status}\n"
            "📅 Участник с: <code>{created_at}</code>"
        ),
        "premium_until": "активен до <b>{expires}</b>",
        "no_premium": "не активен",

        # Shop
        "shop_title": (
            "🛍️ <b>Магазин</b>\n\n"
            "Оформи <b>Премиум</b>:\n"
            "• ⚡ Безлимитная энергия\n"
            "• 💎 Кристаллы для особых сценариев\n\n"
            "Оплата через ⭐ Telegram Stars."
        ),
        "invoice_title": "Velvet Премиум — {label}",
        "invoice_desc": "Безлимитная энергия на {label} + {gems} 💎 кристаллов",
        "payment_ok": (
            "✅ <b>Оплата получена — спасибо!</b>\n\n"
            "⭐ Премиум активен до <b>{expires}</b>\n"
            "💎 <b>+{gems} кристаллов</b> добавлено на счёт!"
        ),

        # Generic
        "back": "← Назад",
        "main_menu_btn": "🏠 Главное меню",
        "reset_chat": "🔄 Сбросить чат",
        "error_generic": "⚠️ Что-то пошло не так. Попробуй ещё раз.",
    },
},
    "uz": {
        # Onboarding
        "choose_lang": "👋 <b>Velvet</b> ga xush kelibsiz!\n\nTilni tanlang:",
        "lang_set": "Til o'rnatildi ✅",

        # Main menu
        "main_menu": (
            "🏠 <b>Asosiy menyu</b>\n\n"
            "⚡ Energiya: <b>{energy}/49</b>  |  💎 Javohirlar: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Premium: <b>faol</b>, {expires} gacha",
        "sub_none": "✨ Premium: <b>faol emas</b>",

        # Characters
        "choose_character": (
            "💬 <b>Qahramonni tanlang</b>\n"
            "Kim bilan vaqt o'tkazmoqchisiz?"
        ),
        "character_card": (
            "{avatar} <b>{name}</b>\n"
            "<i>{tagline}</i>\n\n"
            "🎭 <b>Stsenariyni tanlang:</b>"
        ),
        "not_enough_gems": (
            "💎 <b>Javohirlar yetarli emas!</b>\n\n"
            "Bu stsenariy <b>{cost} javohir</b> turadi.\n"
            "Sizda <b>{gems}</b> bor.\n\n"
            "Ko'proq olish uchun 🛍️ Do'konga boring."
        ),
        "gems_spent": "💎 <b>{cost} javohir</b> sarflandi. Boshlaymiz! ✨",

        # Chat
        "chat_new": "✨ <i>Yangi suhbat boshlanmoqda…</i>",
        "chat_continue": "✨ <i>Suhbat davom ettirilmoqda…</i>",
        "chat_reset_done": "🔄 <i>Chat tozalandi. Qaytadan boshlaymiz…</i>",
        "no_energy": (
            "⚡ <b>Energiya tugadi!</b>\n\n"
            "Energiya har kuni yarim tunda yangilanadi.\n\n"
            "Cheksiz xabarlar uchun <b>Premium</b> oling! ✨"
        ),
        "ai_error": "⚠️ Javob olishning iloji bo'lmadi. Qaytadan urinib ko'ring.",
        "chat_hint": "<i>{name} ga xabar yozing…</i>",

        # Profile
        "profile": (
            "👤 <b>Profilingiz</b>\n\n"
            "⚡ Bugungi energiya: <b>{energy}/49</b>\n"
            "💎 Javohirlar: <b>{gems}</b>\n"
            "✨ Premium: {sub_status}\n"
            "📅 A'zo bo'lgan sana: <code>{created_at}</code>"
        ),
        "premium_until": "{expires} gacha faol",
        "no_premium": "faol emas",

        # Shop
        "shop_title": (
            "🛍️ <b>Do'kon</b>\n\n"
            "<b>Premium</b> oling:\n"
            "• ⚡ Cheksiz kunlik energiya\n"
            "• 💎 Maxsus stsenariylar uchun javohirlar\n\n"
            "⭐ Telegram Stars orqali xavfsiz to'lov."
        ),
        "invoice_title": "Velvet Premium — {label}",
        "invoice_desc": "{label} uchun cheksiz energiya + {gems} 💎 javohir",
        "payment_ok": (
            "✅ <b>To'lov qabul qilindi — rahmat!</b>\n\n"
            "⭐ Premium <b>{expires}</b> gacha faol\n"
            "💎 <b>+{gems} javohir</b> hisobingizga qo'shildi!"
        ),

        # Generic
        "back": "← Orqaga",
        "main_menu_btn": "🏠 Asosiy menyu",
        "reset_chat": "🔄 Chatni tozalash",
        "error_generic": "⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
    },

}


def t(key: str, lang: str = "en", **kwargs: Any) -> str:
    """Return a translated string, falling back to English."""
    lang = lang if lang in STRINGS else "en"
    text: str = STRINGS[lang].get(key) or STRINGS["en"].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    return text
