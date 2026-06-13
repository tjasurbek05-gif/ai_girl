import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, Message,
    LabeledPrice, PreCheckoutQuery,
)

from database import (
    get_user, set_subscription, log_purchase, is_premium,
    add_gems, maybe_award_referral_bonus,
)
from keyboards import (
    shop_keyboard, get_plan_meta, back_to_menu_keyboard,
    gems_store_keyboard, get_gems_pack_meta,
)
from locales import t

logger = logging.getLogger(__name__)
router = Router()

# Days each plan grants
_PLAN_DAYS = {
    "2days":   2,
    "1month":  30,
    "3months": 90,
    "1year":   365,
}

# Invoice payload prefixes (to distinguish payment types)
_PAYLOAD_PREFIX = "velvet_plan:"
_GEMS_PAYLOAD_PREFIX = "velvet_gems:"


async def _notify_referrer(bot, lang_for_self: str, user_id: int) -> None:
    """Award & notify a referrer if this user just made their first purchase."""
    referrer_id = await maybe_award_referral_bonus(user_id, bonus_gems=20)
    if not referrer_id:
        return
    try:
        ref_user = await get_user(referrer_id)
        ref_lang = ref_user["lang"] if ref_user else "en"
        await bot.send_message(referrer_id, t("referral_bonus_awarded", ref_lang, gems=20))
    except Exception:
        logger.exception("Failed to notify referrer %s", referrer_id)


# ── Shop menu ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:shop")
async def cb_shop(callback: CallbackQuery, db_user: dict) -> None:
    lang = db_user["lang"]
    await callback.message.edit_text(
        t("shop_title", lang),
        reply_markup=shop_keyboard(lang),
    )
    await callback.answer()


# ── Buy — send Stars invoice ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("buy:"))
async def cb_buy(callback: CallbackQuery, db_user: dict) -> None:
    plan_key = callback.data.split(":", 1)[1]
    lang = db_user["lang"]
    meta = get_plan_meta(plan_key)

    if not meta:
        await callback.answer(t("error_generic", lang), show_alert=True)
        return

    label  = meta["labels"].get(lang, meta["labels"]["en"])
    stars  = meta["stars"]
    gems   = meta["gems"]

    title   = t("invoice_title", lang, label=label)
    desc    = t("invoice_desc",  lang, label=label, gems=gems)
    payload = f"{_PAYLOAD_PREFIX}{plan_key}"

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title=title,
        description=desc,
        payload=payload,
        currency="XTR",           # Telegram Stars
        prices=[LabeledPrice(label=title, amount=stars)],
        # No provider_token for Stars payments
    )
    await callback.answer()


# ── Gems Store ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:gems_store")
async def cb_gems_store(callback: CallbackQuery, db_user: dict) -> None:
    lang = db_user["lang"]
    await callback.message.edit_text(
        t("gems_store_title", lang),
        reply_markup=gems_store_keyboard(lang),
    )
    await callback.answer()


async def send_gems_invoice(bot, chat_id: int, pack_id: str, lang: str) -> bool:
    """Send a Telegram Stars invoice for a gems pack. Returns False if pack_id unknown."""
    meta = get_gems_pack_meta(pack_id)
    if not meta:
        return False

    title   = t("gems_invoice_title", lang, gems=meta["gems"])
    desc    = t("gems_invoice_desc",  lang, gems=meta["gems"])
    payload = f"{_GEMS_PAYLOAD_PREFIX}{pack_id}"

    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=desc,
        payload=payload,
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=meta["stars"])],
    )
    return True


@router.callback_query(F.data.startswith("buygems:"))
async def cb_buy_gems(callback: CallbackQuery, db_user: dict) -> None:
    pack_id = callback.data.split(":", 1)[1]
    lang = db_user["lang"]
    ok = await send_gems_invoice(callback.bot, callback.from_user.id, pack_id, lang)
    if not ok:
        await callback.answer(t("error_generic", lang), show_alert=True)
        return
    await callback.answer()


# ── Pre-checkout (must answer within 10 s) ────────────────────────────────────

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    # Validate payload belongs to us
    if query.invoice_payload.startswith(_PAYLOAD_PREFIX) or query.invoice_payload.startswith(_GEMS_PAYLOAD_PREFIX):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Unknown payment payload.")


# ── Successful payment ────────────────────────────────────────────────────────

@router.message(F.successful_payment)
async def successful_payment(message: Message, db_user: dict) -> None:
    payload = message.successful_payment.invoice_payload
    lang = db_user["lang"] if db_user else "en"
    user_id = message.from_user.id

    # ── Gems pack purchase ──────────────────────────────────────────────
    if payload.startswith(_GEMS_PAYLOAD_PREFIX):
        pack_key = payload[len(_GEMS_PAYLOAD_PREFIX):]
        meta = get_gems_pack_meta(pack_key)
        if not meta:
            logger.error("Unknown gems pack in successful payment: %s", pack_key)
            await message.answer(t("error_generic", lang))
            return

        stars = message.successful_payment.total_amount
        await add_gems(user_id, meta["gems"])
        await log_purchase(user_id, stars, pack_key, meta["gems"])

        logger.info("Gems payment OK — user=%s pack=%s stars=%s gems=%s", user_id, pack_key, stars, meta["gems"])

        await _notify_referrer(message.bot, lang, user_id)

        await message.answer(
            t("gems_payment_ok", lang, gems=meta["gems"]),
            reply_markup=back_to_menu_keyboard(lang),
        )
        return

    if not payload.startswith(_PAYLOAD_PREFIX):
        return

    plan_key = payload[len(_PAYLOAD_PREFIX):]
    meta = get_plan_meta(plan_key)
    days = _PLAN_DAYS.get(plan_key)

    if not meta or not days:
        logger.error("Unknown plan in successful payment: %s", plan_key)
        await message.answer(t("error_generic", lang))
        return

    stars = message.successful_payment.total_amount
    gems  = meta["gems"]

    # Calculate new expiry — extend if still active
    now = datetime.now()
    user = await get_user(user_id)
    base = now

    if user and user.get("sub_expires"):
        try:
            current_exp = datetime.fromisoformat(user["sub_expires"])
            if current_exp > now:
                base = current_exp  # stack onto existing sub
        except ValueError:
            pass

    new_exp = base + timedelta(days=days)
    expires_str = new_exp.isoformat()
    expires_display = new_exp.strftime("%d %b %Y")

    await set_subscription(user_id, expires_str, gems)
    await log_purchase(user_id, stars, plan_key, gems)

    label = meta["labels"].get(lang, meta["labels"]["en"])
    logger.info(
        "Payment OK — user=%s plan=%s stars=%s gems=%s expires=%s",
        user_id, plan_key, stars, gems, expires_str,
    )

    await _notify_referrer(message.bot, lang, user_id)

    await message.answer(
        t("payment_ok", lang, expires=expires_display, gems=gems),
        reply_markup=back_to_menu_keyboard(lang),
    )
