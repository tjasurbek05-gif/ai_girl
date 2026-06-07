"""
Admin panel handler.
/panel — super admin + granted admins only.

Permission levels:
  Super admin (SUPER_ADMIN_ID in .env):  full access — stats, users, add/remove admins
  Regular admin (admins table):          stats + give gems/sub only
"""

import logging
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import config
from database import (
    is_admin, add_admin, remove_admin, get_admins,
    get_stats, get_user, add_gems, set_subscription, is_premium,
)
from states import PanelStates

logger = logging.getLogger(__name__)
router = Router()

_PLAN_DAYS   = {"2days": 2, "1month": 30, "3months": 90, "1year": 365}
_PLAN_GEMS   = {
    "2days":   config.GEMS_2DAYS,
    "1month":  config.GEMS_1MONTH,
    "3months": config.GEMS_3MONTHS,
    "1year":   config.GEMS_1YEAR,
}
_PLAN_LABELS = {
    "2days": "2 Days", "1month": "1 Month", "3months": "3 Months", "1year": "1 Year"
}


# ── Keyboards ─────────────────────────────────────────────────────────────────

def _main_kb():
    b = InlineKeyboardBuilder()
    b.button(text="📊 Stats",   callback_data="panel:stats")
    b.button(text="👥 Users",   callback_data="panel:users")
    b.button(text="👑 Admins",  callback_data="panel:admins")
    b.button(text="❌ Close",   callback_data="panel:close")
    b.adjust(2, 1, 1)
    return b.as_markup()


def _back_kb():
    b = InlineKeyboardBuilder()
    b.button(text="◀️ Panel", callback_data="panel:main")
    return b.as_markup()


def _users_kb():
    b = InlineKeyboardBuilder()
    b.button(text="💎 Give Gems",  callback_data="panel:give_gems")
    b.button(text="⭐ Give Sub",   callback_data="panel:give_sub")
    b.button(text="◀️ Back",       callback_data="panel:main")
    b.adjust(2, 1)
    return b.as_markup()


def _admins_kb(is_super: bool):
    b = InlineKeyboardBuilder()
    b.button(text="📋 List Admins", callback_data="panel:list_admins")
    if is_super:
        b.button(text="➕ Add Admin",    callback_data="panel:add_admin")
        b.button(text="➖ Remove Admin",  callback_data="panel:remove_admin")
    b.button(text="◀️ Back",            callback_data="panel:main")
    b.adjust(1, 2, 1) if is_super else b.adjust(1)
    return b.as_markup()


def _sub_plans_kb(uid: int):
    """Encode uid in callback data so no FSM state needed for plan selection."""
    b = InlineKeyboardBuilder()
    b.button(text="2 Days",   callback_data=f"panel:sub:{uid}:2days")
    b.button(text="1 Month",  callback_data=f"panel:sub:{uid}:1month")
    b.button(text="3 Months", callback_data=f"panel:sub:{uid}:3months")
    b.button(text="1 Year",   callback_data=f"panel:sub:{uid}:1year")
    b.button(text="❌ Cancel", callback_data="panel:users")
    b.adjust(2, 2, 1)
    return b.as_markup()


# ── Access guard ──────────────────────────────────────────────────────────────

async def _guard(user_id: int, cb: CallbackQuery | None = None) -> bool:
    if await is_admin(user_id):
        return True
    if cb:
        await cb.answer("⛔ Access denied.", show_alert=True)
    return False


# ── /panel command ────────────────────────────────────────────────────────────

@router.message(Command("panel"))
async def cmd_panel(message: Message, state: FSMContext) -> None:
    if not await _guard(message.from_user.id):
        return
    await state.clear()
    await message.answer("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())


# ── Navigation ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:main")
async def cb_main(callback: CallbackQuery, state: FSMContext) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    await state.clear()
    await callback.message.edit_text("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())
    await callback.answer()


@router.callback_query(F.data == "panel:close")
async def cb_close(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.answer()


# ── Stats ─────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:stats")
async def cb_stats(callback: CallbackQuery) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    s = await get_stats()
    text = (
        "📊 <b>Statistics</b>\n\n"
        f"👥 Total users:      <b>{s['total_users']:,}</b>\n"
        f"🆕 New today:        <b>{s['new_today']}</b>\n"
        f"⚡ Active today:     <b>{s['active_today']}</b>\n"
        f"💬 Messages today:   <b>{s['messages_today']}</b>\n"
        f"✨ Premium users:    <b>{s['premium_users']}</b>\n\n"
        f"🛍 Purchases today:  <b>{s['purchases_today']}</b>\n"
        f"⭐ Revenue today:    <b>{s['revenue_today']:,} ⭐</b>\n"
        f"⭐ All-time revenue: <b>{s['revenue_total']:,} ⭐</b>"
    )
    await callback.message.edit_text(text, reply_markup=_back_kb())
    await callback.answer()


# ── Users ─────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:users")
async def cb_users(callback: CallbackQuery, state: FSMContext) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    await state.clear()
    await callback.message.edit_text(
        "👥 <b>User Management</b>", reply_markup=_users_kb()
    )
    await callback.answer()


# Give Gems ───────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:give_gems")
async def cb_give_gems(callback: CallbackQuery, state: FSMContext) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    await state.set_state(PanelStates.waiting_gems_uid)
    await callback.message.edit_text(
        "💎 <b>Give Gems</b>\n\nEnter <b>user ID</b>:\n<i>/cancel to abort</i>",
        reply_markup=_back_kb()
    )
    await callback.answer()


@router.message(PanelStates.waiting_gems_uid, F.text)
async def panel_gems_uid(message: Message, state: FSMContext) -> None:
    if not await _guard(message.from_user.id):
        return
    if message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())
        return
    if not message.text.strip().lstrip("-").isdigit():
        await message.answer("❌ Enter a numeric user ID:")
        return
    uid = int(message.text.strip())
    user = await get_user(uid)
    if not user:
        await message.answer("❌ User not found. Try again:")
        return
    await state.update_data(target_uid=uid)
    await state.set_state(PanelStates.waiting_gems_amount)
    await message.answer(
        f"✅ Found user <code>{uid}</code>\n"
        f"Gems: <b>{user['gems']} 💎</b>\n\n"
        "Enter amount to add <i>(negative to deduct)</i>:\n<i>/cancel to abort</i>"
    )


@router.message(PanelStates.waiting_gems_amount, F.text)
async def panel_gems_amount(message: Message, state: FSMContext) -> None:
    if not await _guard(message.from_user.id):
        return
    if message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())
        return
    if not message.text.strip().lstrip("-").isdigit():
        await message.answer("❌ Enter a number:")
        return
    amount = int(message.text.strip())
    if amount == 0:
        await message.answer("❌ Amount must be non-zero:")
        return
    data = await state.get_data()
    uid = data["target_uid"]
    await add_gems(uid, amount)
    user = await get_user(uid)
    await state.clear()
    sign = "+" if amount > 0 else ""
    await message.answer(
        f"✅ <b>Done!</b>\n\n"
        f"👤 User: <code>{uid}</code>\n"
        f"💎 Change: <b>{sign}{amount}</b>\n"
        f"💎 New balance: <b>{user['gems']}</b>",
        reply_markup=_back_kb()
    )


# Give Subscription ───────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:give_sub")
async def cb_give_sub(callback: CallbackQuery, state: FSMContext) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    await state.set_state(PanelStates.waiting_sub_uid)
    await callback.message.edit_text(
        "⭐ <b>Give Subscription</b>\n\nEnter <b>user ID</b>:\n<i>/cancel to abort</i>",
        reply_markup=_back_kb()
    )
    await callback.answer()


@router.message(PanelStates.waiting_sub_uid, F.text)
async def panel_sub_uid(message: Message, state: FSMContext) -> None:
    if not await _guard(message.from_user.id):
        return
    if message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())
        return
    if not message.text.strip().lstrip("-").isdigit():
        await message.answer("❌ Invalid ID. Try again:")
        return
    uid = int(message.text.strip())
    user = await get_user(uid)
    if not user:
        await message.answer("❌ User not found. Try again:")
        return
    await state.clear()
    premium = await is_premium(uid)
    status = "✨ Premium" if premium else "Free"
    await message.answer(
        f"✅ Found user <code>{uid}</code>\n"
        f"Status: <b>{status}</b>\n\n"
        "Choose subscription plan:",
        reply_markup=_sub_plans_kb(uid)
    )


@router.callback_query(F.data.startswith("panel:sub:"))
async def cb_sub_plan(callback: CallbackQuery) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    # format: panel:sub:{uid}:{plan}
    parts = callback.data.split(":")
    if len(parts) != 4:
        await callback.answer("Invalid data.", show_alert=True)
        return
    try:
        uid = int(parts[2])
    except ValueError:
        await callback.answer("Invalid user ID.", show_alert=True)
        return
    plan = parts[3]
    days = _PLAN_DAYS.get(plan)
    gems = _PLAN_GEMS.get(plan)
    if not days:
        await callback.answer("Invalid plan.", show_alert=True)
        return
    user = await get_user(uid)
    if not user:
        await callback.answer("User not found.", show_alert=True)
        return

    # Stack on top of existing sub if still active
    now = datetime.now()
    base = now
    if user.get("sub_expires"):
        try:
            exp = datetime.fromisoformat(user["sub_expires"])
            if exp > now:
                base = exp
        except ValueError:
            pass

    new_exp = base + timedelta(days=days)
    await set_subscription(uid, new_exp.isoformat(), gems)

    label = _PLAN_LABELS.get(plan, plan)
    await callback.message.edit_text(
        f"✅ <b>Subscription granted!</b>\n\n"
        f"👤 User: <code>{uid}</code>\n"
        f"📅 Plan: <b>{label}</b>\n"
        f"⏳ Expires: <b>{new_exp.strftime('%d %b %Y')}</b>\n"
        f"💎 Gems added: <b>+{gems}</b>",
        reply_markup=_back_kb()
    )
    await callback.answer("Done! ✅")


# ── Admins ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "panel:admins")
async def cb_admins(callback: CallbackQuery) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    is_super = callback.from_user.id == config.SUPER_ADMIN_ID
    await callback.message.edit_text(
        "👑 <b>Admin Management</b>",
        reply_markup=_admins_kb(is_super)
    )
    await callback.answer()


@router.callback_query(F.data == "panel:list_admins")
async def cb_list_admins(callback: CallbackQuery) -> None:
    if not await _guard(callback.from_user.id, callback):
        return
    admins = await get_admins()
    if not admins:
        lines = "No admins added yet."
    else:
        lines = "\n".join(
            f"• <code>{a['user_id']}</code>  (added by <code>{a['added_by']}</code>)"
            for a in admins
        )
    text = (
        f"👑 <b>Admins</b>\n\n{lines}\n\n"
        f"🔑 Super admin: <code>{config.SUPER_ADMIN_ID}</code>"
    )
    await callback.message.edit_text(text, reply_markup=_back_kb())
    await callback.answer()


@router.callback_query(F.data == "panel:add_admin")
async def cb_add_admin(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.from_user.id != config.SUPER_ADMIN_ID:
        await callback.answer("⛔ Super admin only.", show_alert=True)
        return
    await state.set_state(PanelStates.waiting_new_admin_uid)
    await callback.message.edit_text(
        "➕ <b>Add Admin</b>\n\n"
        "Enter the <b>user ID</b> to promote:\n<i>/cancel to abort</i>",
        reply_markup=_back_kb()
    )
    await callback.answer()


@router.message(PanelStates.waiting_new_admin_uid, F.text)
async def panel_add_admin_uid(message: Message, state: FSMContext) -> None:
    if message.from_user.id != config.SUPER_ADMIN_ID:
        return
    if message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("🎛 <b>Admin Panel</b>", reply_markup=_main_kb())
        return
    if not message.text.strip().lstrip("-").isdigit():
        await message.answer("❌ Invalid ID:")
        return
    uid = int(message.text.strip())
    if uid == config.SUPER_ADMIN_ID:
        await message.answer("❌ Already the super admin.")
        return
    user = await get_user(uid)
    if not user:
        await message.answer("❌ User not found (they must start the bot first):")
        return
    await add_admin(uid, message.from_user.id)
    await state.clear()
    await message.answer(
        f"✅ <b>Done!</b>\n\n"
        f"User <code>{uid}</code> is now an admin.",
        reply_markup=_back_kb()
    )


@router.callback_query(F.data == "panel:remove_admin")
async def cb_remove_admin_list(callback: CallbackQuery) -> None:
    if callback.from_user.id != config.SUPER_ADMIN_ID:
        await callback.answer("⛔ Super admin only.", show_alert=True)
        return
    admins = await get_admins()
    if not admins:
        await callback.answer("No admins to remove.", show_alert=True)
        return
    b = InlineKeyboardBuilder()
    for a in admins:
        b.button(text=f"🗑 {a['user_id']}", callback_data=f"panel:rmadmin:{a['user_id']}")
    b.button(text="◀️ Back", callback_data="panel:admins")
    b.adjust(1)
    await callback.message.edit_text(
        "➖ <b>Remove Admin</b>\n\nTap an admin to remove:",
        reply_markup=b.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("panel:rmadmin:"))
async def cb_do_remove_admin(callback: CallbackQuery) -> None:
    if callback.from_user.id != config.SUPER_ADMIN_ID:
        await callback.answer("⛔ Super admin only.", show_alert=True)
        return
    uid = int(callback.data.split(":")[-1])
    await remove_admin(uid)
    await callback.answer(f"✅ Admin {uid} removed.", show_alert=True)
    # Refresh the remove list
    admins = await get_admins()
    if not admins:
        await callback.message.edit_text(
            "👑 <b>Admin Management</b>\n\nNo more admins.",
            reply_markup=_admins_kb(True)
        )
        return
    b = InlineKeyboardBuilder()
    for a in admins:
        b.button(text=f"🗑 {a['user_id']}", callback_data=f"panel:rmadmin:{a['user_id']}")
    b.button(text="◀️ Back", callback_data="panel:admins")
    b.adjust(1)
    await callback.message.edit_text(
        "➖ <b>Remove Admin</b>\n\nTap an admin to remove:",
        reply_markup=b.as_markup()
    )
