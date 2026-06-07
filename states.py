from aiogram.fsm.state import State, StatesGroup


class ChatStates(StatesGroup):
    chatting = State()


class PanelStates(StatesGroup):
    waiting_gems_uid      = State()
    waiting_gems_amount   = State()
    waiting_sub_uid       = State()
    waiting_new_admin_uid = State()
