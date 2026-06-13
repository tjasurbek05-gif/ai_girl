from typing import Any

STRINGS: dict[str, dict[str, Any]] = {
    "en": {
        "choose_lang": "👋 Welcome to <b>Velvet</b>!\n\nChoose your language:",
        "lang_set": "Language set ✅",
        "main_menu": (
            "🏠 <b>Main Menu</b>\n\n"
            "⚡ Energy: <b>{energy}/49</b>  |  💎 Gems: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Premium: <b>active</b> until {expires}",
        "sub_none": "✨ Premium: <b>not active</b>",
        "choose_character": "💬 <b>Choose a character</b>\nWho would you like to spend time with?",
        "character_card": "{avatar} <b>{name}</b>\n<i>{tagline}</i>\n\n🎭 <b>Choose a scenario:</b>",
        "not_enough_gems": (
            "💎 <b>Not enough gems!</b>\n\n"
            "This scenario costs <b>{cost} gems</b>.\n"
            "You have <b>{gems}</b>.\n\nVisit the 🛍️ Shop to get more."
        ),
        "gems_spent": "💎 <b>{cost} gems</b> spent. Let's begin! ✨",
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
        "profile": (
            "👤 <b>Your Profile</b>\n\n"
            "⚡ Energy today: <b>{energy}/49</b>\n"
            "💎 Gems: <b>{gems}</b>\n"
            "✨ Premium: {sub_status}\n"
            "📅 Member since: <code>{created_at}</code>"
        ),
        "premium_until": "active until <b>{expires}</b>",
        "no_premium": "not active",
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
        "back": "← Back",
        "main_menu_btn": "🏠 Main Menu",
        "reset_chat": "🔄 Reset chat",
        "error_generic": "⚠️ Something went wrong. Please try again.",
        "gems_store_title": (
            "💎 <b>Gems Store</b>\n\n"
            "Buy gems directly with ⭐ Telegram Stars — use them to unlock special scenarios and shop items."
        ),
        "gems_invoice_title": "Velvet — {gems} Gems",
        "gems_invoice_desc": "Get {gems} 💎 gems added to your account instantly.",
        "gems_payment_ok": "✅ <b>Payment received!</b>\n\n💎 <b>+{gems} gems</b> added to your account!",
        "animate_btn": "🎬 Animate",
        "animate_unavailable": "🎬 No image available yet for this scene to animate.",
        "animate_processing": "🎬 Animating... this may take a moment.",
        "animate_done": "🎬 Here's your animation!",
        "animate_soon": "🎬 Animations are coming soon! Stay tuned ✨",
        "referral_bonus_awarded": "🤝 <b>+{gems} gems</b> — a friend you invited just made a purchase!",
        "affiliate_card": (
            "🤝 <b>Affiliate Program</b>\n\n"
            "Invite friends and earn 💎 gems when they make their first purchase!\n\n"
            "Your link:\n<code>{link}</code>\n\n"
            "👥 Referrals: <b>{count}</b>\n"
            "💎 Earned: <b>{earned}</b>"
        ),
        "custom_character_soon": (
            "✨ <b>Custom characters are coming soon!</b>\n\n"
            "This premium feature will let you build any companion you want for 99 💎. Stay tuned!"
        ),
        "reengagement_msg": (
            "💌 Hey... it's been a while! <b>{name}</b> is waiting for you in your "
            "<b>{scenario}</b> story. Come back? 🥺"
        ),
    },
    "ru": {
        "choose_lang": "👋 Добро пожаловать в <b>Velvet</b>!\n\nВыбери язык:",
        "lang_set": "Язык установлен ✅",
        "main_menu": (
            "🏠 <b>Главное меню</b>\n\n"
            "⚡ Энергия: <b>{energy}/49</b>  |  💎 Кристаллы: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Премиум: <b>активен</b> до {expires}",
        "sub_none": "✨ Премиум: <b>не активен</b>",
        "choose_character": "💬 <b>Выбери персонажа</b>\nС кем хочешь провести время?",
        "character_card": "{avatar} <b>{name}</b>\n<i>{tagline}</i>\n\n🎭 <b>Выбери сценарий:</b>",
        "not_enough_gems": (
            "💎 <b>Недостаточно кристаллов!</b>\n\n"
            "Этот сценарий стоит <b>{cost} кристаллов</b>.\n"
            "У тебя <b>{gems}</b>.\n\nЗайди в 🛍️ Магазин, чтобы получить больше."
        ),
        "gems_spent": "💎 Потрачено <b>{cost} кристаллов</b>. Начинаем! ✨",
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
        "profile": (
            "👤 <b>Твой профиль</b>\n\n"
            "⚡ Энергия сегодня: <b>{energy}/49</b>\n"
            "💎 Кристаллы: <b>{gems}</b>\n"
            "✨ Премиум: {sub_status}\n"
            "📅 Участник с: <code>{created_at}</code>"
        ),
        "premium_until": "активен до <b>{expires}</b>",
        "no_premium": "не активен",
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
        "back": "← Назад",
        "main_menu_btn": "🏠 Главное меню",
        "reset_chat": "🔄 Сбросить чат",
        "error_generic": "⚠️ Что-то пошло не так. Попробуй ещё раз.",
        "gems_store_title": (
            "💎 <b>Магазин кристаллов</b>\n\n"
            "Покупай кристаллы напрямую за ⭐ Telegram Stars — открывай особые сценарии и предметы."
        ),
        "gems_invoice_title": "Velvet — {gems} кристаллов",
        "gems_invoice_desc": "Получи {gems} 💎 кристаллов на свой счёт мгновенно.",
        "gems_payment_ok": "✅ <b>Оплата получена!</b>\n\n💎 <b>+{gems} кристаллов</b> добавлено на счёт!",
        "animate_btn": "🎬 Анимация",
        "animate_unavailable": "🎬 Для этой сцены пока нет изображения для анимации.",
        "animate_processing": "🎬 Создаём анимацию... это может занять момент.",
        "animate_done": "🎬 Вот твоя анимация!",
        "animate_soon": "🎬 Анимации скоро появятся! Следи за обновлениями ✨",
        "referral_bonus_awarded": "🤝 <b>+{gems} кристаллов</b> — друг, которого ты пригласил, совершил покупку!",
        "affiliate_card": (
            "🤝 <b>Партнёрская программа</b>\n\n"
            "Приглашай друзей и получай 💎 кристаллы за их первую покупку!\n\n"
            "Твоя ссылка:\n<code>{link}</code>\n\n"
            "👥 Приглашено: <b>{count}</b>\n"
            "💎 Заработано: <b>{earned}</b>"
        ),
        "custom_character_soon": (
            "✨ <b>Свои персонажи скоро появятся!</b>\n\n"
            "Эта премиум-функция позволит создать любого персонажа за 99 💎. Следи за обновлениями!"
        ),
        "reengagement_msg": (
            "💌 Привет... давно не виделись! <b>{name}</b> ждёт тебя в истории "
            "<b>{scenario}</b>. Вернёшься? 🥺"
        ),
    },
    "uz": {
        "choose_lang": "👋 <b>Velvet</b> ga xush kelibsiz!\n\nTilni tanlang:",
        "lang_set": "Til o'rnatildi ✅",
        "main_menu": (
            "🏠 <b>Asosiy menyu</b>\n\n"
            "⚡ Energiya: <b>{energy}/49</b>  |  💎 Javohirlar: <b>{gems}</b>\n"
            "{sub_line}"
        ),
        "sub_active": "✨ Premium: <b>faol</b>, {expires} gacha",
        "sub_none": "✨ Premium: <b>faol emas</b>",
        "choose_character": "💬 <b>Qahramonni tanlang</b>\nKim bilan vaqt o'tkazmoqchisiz?",
        "character_card": "{avatar} <b>{name}</b>\n<i>{tagline}</i>\n\n🎭 <b>Stsenariyni tanlang:</b>",
        "not_enough_gems": (
            "💎 <b>Javohirlar yetarli emas!</b>\n\n"
            "Bu stsenariy <b>{cost} javohir</b> turadi.\n"
            "Sizda <b>{gems}</b> bor.\n\nKo'proq olish uchun 🛍️ Do'konga boring."
        ),
        "gems_spent": "💎 <b>{cost} javohir</b> sarflandi. Boshlaymiz! ✨",
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
        "profile": (
            "👤 <b>Profilingiz</b>\n\n"
            "⚡ Bugungi energiya: <b>{energy}/49</b>\n"
            "💎 Javohirlar: <b>{gems}</b>\n"
            "✨ Premium: {sub_status}\n"
            "📅 A'zo bo'lgan sana: <code>{created_at}</code>"
        ),
        "premium_until": "{expires} gacha faol",
        "no_premium": "faol emas",
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
        "back": "← Orqaga",
        "main_menu_btn": "🏠 Asosiy menyu",
        "reset_chat": "🔄 Chatni tozalash",
        "error_generic": "⚠️ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
        "gems_store_title": (
            "💎 <b>Gemlar do'koni</b>\n\n"
            "⭐ Telegram Stars orqali gemlar sotib oling — maxsus stsenariy va buyumlarni oching."
        ),
        "gems_invoice_title": "Velvet — {gems} gem",
        "gems_invoice_desc": "Hisobingizga {gems} 💎 gem darhol qo'shiladi.",
        "gems_payment_ok": "✅ <b>To'lov qabul qilindi!</b>\n\n💎 <b>+{gems} gem</b> hisobingizga qo'shildi!",
        "animate_btn": "🎬 Animatsiya",
        "animate_unavailable": "🎬 Bu sahna uchun hali animatsiya qilish uchun rasm yo'q.",
        "animate_processing": "🎬 Animatsiya yaratilmoqda... bu biroz vaqt olishi mumkin.",
        "animate_done": "🎬 Mana sizning animatsiyangiz!",
        "animate_soon": "🎬 Animatsiyalar tez orada qo'shiladi! Kuzatib boring ✨",
        "referral_bonus_awarded": "🤝 <b>+{gems} gem</b> — taklif qilgan do'stingiz xarid qildi!",
        "affiliate_card": (
            "🤝 <b>Hamkorlik dasturi</b>\n\n"
            "Do'stlarni taklif qiling va ularning birinchi xaridi uchun 💎 gem oling!\n\n"
            "Sizning havolangiz:\n<code>{link}</code>\n\n"
            "👥 Taklif qilinganlar: <b>{count}</b>\n"
            "💎 Ishlangan: <b>{earned}</b>"
        ),
        "custom_character_soon": (
            "✨ <b>O'z qahramonlaringiz tez orada!</b>\n\n"
            "Bu premium funksiya 99 💎 evaziga istalgan qahramonni yaratish imkonini beradi. Kuzatib boring!"
        ),
        "reengagement_msg": (
            "💌 Salom... ko'rishmaganimizga ancha bo'ldi! <b>{name}</b> sizni "
            "<b>{scenario}</b> hikoyasida kutmoqda. Qaytib kelasizmi? 🥺"
        ),
    },
}


def t(key: str, lang: str = "en", **kwargs: Any) -> str:
    lang = lang if lang in STRINGS else "en"
    text: str = STRINGS[lang].get(key) or STRINGS["en"].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass
    return text
