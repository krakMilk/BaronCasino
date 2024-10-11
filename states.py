from aiogram.dispatcher.filters.state import StatesGroup, State

class search_ref(StatesGroup):
    start = State()

class ControlUser(StatesGroup):
    start = State()

class SendMessage(StatesGroup):
    start = State()

class ChangeMax(StatesGroup):
    start = State()

class ChangeInvoice(StatesGroup):
    start = State()

class Deposit(StatesGroup):
    start = State()

class Broadcast(StatesGroup):
    start = State()

class Withdraw(StatesGroup):
    start = State()