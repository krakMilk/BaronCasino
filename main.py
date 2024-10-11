import re
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher, Bot, executor
import requests
import string
import random
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from datetime import datetime
import asyncio
import bet_sender
import os
import kb
import config
import sqlite3
import states
import asyncio
from bet_sender import app 

# логирование
logging.basicConfig(level=logging.INFO)

# дисп
bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# обработчики событий( если будут нужны)
# Например dp.register_message_handler(...)

async def on_startup(dp):
    logging.info("Bot is starting...")

if __name__ == "__main__":
    # Запуск бота и диспа
    from bet_sender import app  # Имп app 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
COEFFICIENTS = {
    'победа 1': 1.85,
    'победа 2': 1.85,
    'п1': 1.85,
    'п2': 1.85,
    'ничья': 1.9,
    'нечет': 1.85,
    'фут гол': 1.4,
    'фут мимо': 1.4,
    'баскет гол': 1.4,
    'баскет мимо': 1.4,
    'больше': 1.85,
    'меньше': 1.85,
    'чет': 1.85,
    'дартс белое': 1.5,
    'дартс ред': 1.5,
    'дартс мимо': 1.5,
    'дартс центр': 1.5,
    'камень': 1.6,
    'ножницы': 1.6,
    'бумага': 1.6,
    'сектор 1': 1.85,
    'сектор 2': 1.65,
    'сектор 3': 1.5,
    'пвп': 1.9,
    'красное': 1.8,
    'черное': 1.8,
    'зеро': 2,
    'плинко': 1.8,
}

DICE_CONFIG = {
    'нечет': ("🎲", [1, 3, 5]),
    'баскет гол': ("🏀", [4, 5, 6]),
    'баскет мимо': ("🏀", [1, 2, 3]),
    'больше': ("🎲", [4, 5, 6]),
    'меньше': ("🎲", [1, 2, 3]),
    'чет': ("🎲", [2, 4, 6]),
    'дартс белое': ("🎯", [3, 5]),
    'дартс ред': ("🎯", [2, 4]),
    'дартс мимо': ("🎯", [1]),
    'дартс центр': ("🎯", [6]),
    'сектор 1': ("🎲", [1, 2]),
    'сектор 2': ("🎲", [3, 4]),
    'сектор 3': ("🎲", [3, 4]),
    'плинко': ("🎲", [4, 5, 6]),
    'бумага': ("✋", ['👊']),
    'камень': ("👊", ['✌️']),
    'ножницы': ("✌️", ['✋']),
    'победа 1': ("🎲", [1]),
    'победа 2': ("🎲", [1]),
    'п1': ("🎲", [1]),
    'п2': ("🎲", [1]),
    'ничья': ("🎲", [1]),
    'красное': ("x", ['CAACAgIAAxkBAAEMc65miwstwNiEg2zA8AJbzcIRFqMC1wACa0wAAoogUEqSy15B1lxZkTUE', 'CAACAgIAAxkBAAEMc7Bmiwsw5IM2WLQueYYdK2HXwMXHgwACa04AAusJUEpRWiMnFgPASzUE', 'CAACAgIAAxkBAAEMc7JmiwsylE4VF6vL0VKQhOf3VAaG9QACxk0AAvLaUUpl9jec4WWwkjUE', 'CAACAgIAAxkBAAEMc7Rmiws0EbYpC6loRqTpGMYWgSYwhwAC0kUAAlEuWUoAAeD330H2Uo01BA', 'CAACAgIAAxkBAAEMc7Zmiws2OK79q4iBmNtvUEDKychXlQACiUEAAkhJWUoHGtNoD3zTsDUE', 'CAACAgIAAxkBAAEMc7hmiws4b6CMD27Ocb5JsfQru-0E1AAC8kAAAiPSWUqDQLIJCcw4sTUE', 'CAACAgIAAxkBAAEMc7pmiws6rxpfhd-qW69pOKIF6QJvBwACw1EAAv0eWEqm1mam-L-5JTUE', 'CAACAgIAAxkBAAEMc7xmiws9hFHdEH42J6N2Yuql4eiKlQACoEcAAl5EWUqVzM66FWlaaDUE', 'CAACAgIAAxkBAAEMc75miws_OPGOlsSJO4vZ_4I99pVXMgACgkwAAtR4WUqSD7f4umsywzUE', 'CAACAgIAAxkBAAEMc8BmiwtBrrsLb9mnrJa6sE2z4scZPwACSE8AAoPtUUqiMruDVUZ1SDUE', 'CAACAgIAAxkBAAEMc8JmiwtDwziyzQ_m0DVi5ppT9WZF5gACvUwAA-FRSlhShWr5KKbXNQQ', 'CAACAgIAAxkBAAEMc8RmiwtFKMVO7vkopyNJ794RfOb9PAACz0UAAjV4WEr_1EXGVH2xoTUE', 'CAACAgIAAxkBAAEMc8ZmiwtH0AkS-CF8v3NoxNr1xsJyHAAC600AAobmWEooNhEix_a6mDUE', 'CAACAgIAAxkBAAEMc8hmiwtJVJWO4fXloiDs8gXiFXEvdwAC00AAAuweWEpbjeobSqzftDUE', 'CAACAgIAAxkBAAEMc8pmiwtLvUsHgZy78_E69KAvbl54pgAC6EEAAid_WUp7iVzaYV8_AzUE', 'CAACAgIAAxkBAAEMc8xmiwtO9qq-te18EyK6BwXmCVpyNwAC8VMAAjzjWEoJpnR_Gp2vRzUE', 'CAACAgIAAxkBAAEMc85miwtQ8KAsKiVst0HFCHze24A8LwAC-UYAAulWWEphBgerbGYOITUE', 'CAACAgIAAxkBAAEMc9BmiwtS-lgvkhdM8ZnuZI01RMNtSwACpUsAAp0pWUrIAAEyPwZzvzk1BA']),
    'черное': ("x", ['CAACAgIAAxkBAAEMc9JmiwvYb13xL2TAPvZ5qJedyhr7kQACq1AAAsg8WUraWoiatb18GDUE', 'CAACAgIAAxkBAAEMc9Rmiwvb-YQ1vX3o-N0rM3vny-bKDAACFksAAj60UEo229Tfsbc5QjUE', 'CAACAgIAAxkBAAEMc9ZmiwvdoueCwSuuX1iqG_kEOLFyqQACy1AAAjj_UUrCBC92XVbpfDUE', 'CAACAgIAAxkBAAEMc9ZmiwvdoueCwSuuX1iqG_kEOLFyqQACy1AAAjj_UUrCBC92XVbpfDUE', 'CAACAgIAAxkBAAEMc9hmiwvgTAfQhMoSdfT0xodUNR__0wACj08AAsBIUEo39mSM5q5B9DUE', 'CAACAgIAAxkBAAEMc9pmiwvi9CziyEkW85HBfYCVCvSLbQAC5VEAAkrJUUqgM9OL3fCB2TUE', 'CAACAgIAAxkBAAEMc9xmiwvkQnSM9QNA3LyHxhnf4KqUWgACgEAAAknlWEq8GP_mPFMm3TUE', 'CAACAgIAAxkBAAEMc95miwvm09G5XskBW2abHVQdM0GYHQACLEcAAlrbWUoi1YY6EOFq9zUE', 'CAACAgIAAxkBAAEMc-BmiwvoJX5WAb-NsTofxwGVnE7S5gAChT8AAmaFWEqEpRMkssTyhzUE', 'CAACAgIAAxkBAAEMc-JmiwvqipfCnF_XuyiFJhrR7zKHSwACeUUAAkyFWEoBVKx02Trj-DUE', 'CAACAgIAAxkBAAEMc-RmiwvsOYYRn2bwss23v0ONpgW6hAACEkUAAhS9WEq7zrdRmpKo1TUE', 'CAACAgIAAxkBAAEMc-Zmiwvu4oEZ9NWyyr9ylU7gdBUpUwACvVUAAmRIWUpdaTruYoIiRzUE', 'CAACAgIAAxkBAAEMc-hmiwvwee89Me_0nQjKtDO02MNQTQACVE8AAkFDUErPxTJG2opUpDUE', 'CAACAgIAAxkBAAEMc-pmiwvyzcxlebbyvQYQp7_yZCRFGAACiUwAAj83WEoxbzqmdO_2BzUE', 'CAACAgIAAxkBAAEMc-xmiwvzstn9eTpOQ2rZLfp0FgUOqQACU0IAAj9nWErmrudsEouYuzUE', 'CAACAgIAAxkBAAEMc-5miwv1iBk0ASnuIIbVFC6eyYdVIwACrGMAAquXWUp00Cv45-WZzjUE', 'CAACAgIAAxkBAAEMc_Bmiwv3-TrgGw8be2zEo5YauxWn-QAC4VIAAoEtWEr0-v_e-Xk48zUE', 'CAACAgIAAxkBAAEMc_Jmiwv51KafJn6br6P8PwyVD4tOvQAC2UQAAvmlWUqjIfPUbYdAMzUE', 'CAACAgIAAxkBAAEMc_Rmiwv7U9S39tedvcUsJovrlYjYQAACtE8AAmMwUUoYWzy8PvnZJTUE']),
    'зеро': ("x", ['CAACAgIAAxkBAAEMc_ZmiwxnGg-LEWkW8GszyZNxtOaUGgACMEYAAnEeWErMXjdnKkjeeTUE']),
    'пвп': ("🎲", [1])
}

# Функции

# Калькуляция винрейта
def calculate_winrate(winning_bets, total_bets):
    if total_bets == 0:
        return 0
    winrate = (winning_bets / total_bets) * 100
    return winrate

# Генерация клавиатуры с рефералами
def generate_keyboard(page: int, refs: list, total_pages: int, per_page: int):
    start = (page - 1) * per_page
    end = start + per_page
    keyb = types.InlineKeyboardMarkup(row_width=2)
    keyb.add(types.InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='empty_button'))
    btns = []

    for ref in refs[start:end]:
        btns.append(types.InlineKeyboardButton(text=ref[6], callback_data=f'empty_button'))

    keyb.add(*btns)

    if page > 1:
        keyb.add(types.InlineKeyboardButton(text="◀️", callback_data=f'page_{page - 1}'))
    if page < total_pages:
        keyb.add(types.InlineKeyboardButton(text="▶️", callback_data=f'page_{page + 1}'))

    keyb.add(types.InlineKeyboardButton(text="🔍 Поиск", callback_data='search_refferals'), 
           types.InlineKeyboardButton(text="◀️ Назад", callback_data='ref_panel'))

    return keyb

# Генерация текста дней
def days_text(days):
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день"
    elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
        return f"{days} дня"
    else:
        return f"{days} дней"

# Функции криптопей

# Генерация рандомного кода для перевода
def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Создание счета для пополнения баланса или же казны
def create_invoice(amount):
    headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
    data = {"asset": "USDT", "amount": float(amount)}
    r = requests.get("https://pay.crypt.bot/api/createInvoice", data=data, headers=headers).json()
    return r['result']['bot_invoice_url']

# Получение баланса или же казны
def get_cb_balance():
    headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
    r = requests.get("https://pay.crypt.bot/api/getBalance", headers=headers).json()
    for currency_data in r['result']:
        if currency_data['currency_code'] == 'USDT':
            usdt_balance = currency_data['available']
            break
    return usdt_balance

# Трансфер или же по простому перевод
async def transfer(amount, us_id):
    bal = get_cb_balance()
    bal = float(bal)
    amount = float(amount)
    keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Закрыть", callback_data='close'))
    keyb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💼 Перейти к пользователю", url=f"tg://user?id={us_id}"))
    if bal < amount:
        try:
            await bot.send_message(us_id, f"<b>[🔔] Вам пришло системное уведомление:</b>\n\n<b><blockquote>Ваша выплата ⌊ {amount}$ ⌉ будет зачислена вручную администратором!</blockquote></b>", reply_markup=keyb)
        except:
            pass
        await bot.send_message(config.LOGS_ID, f"<b>[🔔] Мало суммы в казне для выплаты!</b>\n\n<b><blockquote>Пользователь: {us_id}\nСумма: {amount}$</blockquote></b>", reply_markup=keyb)
        return
    try:
        spend_id = generate_random_code(length=10)
        headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
        data = {"asset": "USDT", "amount": float(amount), "user_id": us_id, "spend_id": spend_id}
        requests.get("https://pay.crypt.bot/api/transfer", data=data, headers=headers)
        await bot.send_message(config.LOGS_ID, f"<b>[🧾] Перевод!</b>\n\n<b>[💠] Сумма: {amount} USDT</b>\n<b>[🚀] Пользователю: {us_id}</b>", reply_markup=keyb)
    except Exception as e:
        print(e)
        return e

# Создание чека
async def create_check(amount, userid):
    bal = get_cb_balance()
    bal = float(bal)
    amount = float(amount)
    keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Закрыть", callback_data='close'))
    keyb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💼 Перейти к пользователю", url=f"tg://user?id={userid}"))
    if bal < amount:
        try:
            await bot.send_message(userid, f"<b>[🔔] Вам пришло системное уведомление:</b>\n\n<b><blockquote>Ваша выплата ⌊ {amount}$ ⌉ будет зачислена вручную администратором!</blockquote></b>", reply_markup=keyb)
        except:
            pass
        await bot.send_message(config.LOGS_ID, f"<b>[🔔] Мало суммы в казне для выплаты!</b>\n\n<b><blockquote>Пользователь: {userid}\nСумма: {amount}$</blockquote></b>", reply_markup=keyb)
        return
    headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
    data = {"asset": "USDT", "amount": float(amount), "pin_to_user_id": userid}
    r = requests.get("https://pay.crypt.bot/api/createCheck", headers=headers, data=data).json()
    await bot.send_message(config.LOGS_ID, f"<b>[🧾] Создан чек!</b>\n\n<b>[💠] Сумма: {amount} USDT</b>\n<b>[🚀] Прикрепен за юзером: {userid}</b>", reply_markup=keyb)
    return r["result"]["bot_check_url"]

# Конвертация USD -> RUB
async def convert(amount_usd):
    headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
    r = requests.get("https://pay.crypt.bot/api/getExchangeRates", headers=headers).json()
    for data in r['result']:
        if data['source'] == 'USDT' and data['target'] == 'RUB':
            rate = data['rate']
            amount_rub = float(amount_usd) * float(rate)
    return amount_rub

# Проверка подписки
async def is_subscribed_to_channel(user_id, mention):
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        exist = cursor.execute("SELECT * FROM users WHERE us_id=?", (user_id,)).fetchone()
        if not exist:
            cursor.execute("INSERT INTO users(us_id,username) VALUES(?,?)", (user_id,mention,))
            conn.commit()
        user = cursor.execute("SELECT * FROM users WHERE us_id=?", (user_id,)).fetchone()
    try:
        chat_id = config.CHANNEL_ID
        check_member = await bot.get_chat_member(chat_id, user_id)
        if check_member.status not in ["member", "administrator", "creator"]:
            return False
        else:
            return True
    except:
        pass

# Команды бота

# /start
@dp.message_handler(commands=['start'], state='*')
async def poshel_nahuy_telebot(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        msg_id = data.get('msg_id')
        await bot.delete_message(message.chat.id, msg_id)
    except:
        pass

    await state.finish()

    try:
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            msg_id = cursor.execute("SELECT msg_id FROM users WHERE us_id=?", (message.from_user.id,)).fetchone()[0]
        await bot.delete_message(message.chat.id, msg_id)
    except:
        pass

    args = message.get_args()
    if args:
        if args.startswith('ref_'):
            referrer = args.split("ref_")[1]
            if message.from_user.id == referrer:
                pass
            else:
                with sqlite3.connect("db.db") as conn:
                    cursor = conn.cursor()
                    exist = cursor.execute("SELECT * FROM users WHERE us_id=?", (message.from_user.id,)).fetchone()
                if exist:
                    pass
                else:
                    with sqlite3.connect("db.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO users(us_id,username,ref) VALUES(?,?,?)", (message.from_user.id,message.from_user.mention,referrer,))
                        conn.commit()
                    await bot.send_message(referrer, f"<blockquote><b>⚡️ У вас новый реферал!\n└ {message.from_user.mention}</b></blockquote>")
                    pass

        else:
            pass
    else:
        pass

    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        exist = cursor.execute("SELECT * FROM users WHERE us_id=?", (message.from_user.id,)).fetchone()
        if not exist:
            cursor.execute("INSERT OR IGNORE INTO users(us_id,username) VALUES(?,?)", (message.from_user.id,message.from_user.mention,))
        else:
            cursor.execute("UPDATE users SET username=? WHERE us_id=?", (message.from_user.mention,message.from_user.id,))
        conn.commit()

        total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE us_id=?", (message.from_user.id,)).fetchone()[0]
        if not total_bets_summ:
            total_bets_summ = float(0.00)
            total_bets_summ = f"{total_bets_summ:.2f}"
        else:
            total_bets_summ = float(total_bets_summ)
            total_bets_summ = f"{total_bets_summ:.2f}"
        
        total_wins_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1 AND us_id=?", (message.from_user.id,)).fetchone()[0]
        if not total_wins_summ:
            total_wins_summ = float(0.00)
            total_wins_summ = f"{total_wins_summ:.2f}"
        else:
            total_wins_summ = float(total_wins_summ)
            total_wins_summ = f"{total_wins_summ:.2f}"
        
        total_lose_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE lose=1 AND us_id=?", (message.from_user.id,)).fetchone()[0]
        if not total_lose_summ:
            total_lose_summ = float(0.00)
            total_lose_summ = f"{total_lose_summ:.2f}"
        else:
            total_lose_summ = float(total_lose_summ)
            total_lose_summ = f"{total_lose_summ:.2f}"

    check = await is_subscribed_to_channel(message.from_user.id, message.from_user.mention)

    if check:
        msg = await message.answer(f"<blockquote><b>👋 Добро пожаловать в реферального бота {config.CASINO_NAME}!\n\n🎲 Статистика ваших ставок\n├ Общая сумма ставок - {total_bets_summ}$\n├ Сумма выигрышей - {total_wins_summ}$\n└ Сумма проигрышей - {total_lose_summ}$</b></blockquote>", reply_markup=kb.menu(message.from_user.id))
    else:
        keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("⚡️ Подписаться", url=config.BETS_LINK))
        msg = await message.answer("<blockquote><b>❌ Чтобы продолжить вы должны быть подписаными на канал ставок, после того как вы подписались пропишите заново /start</b></blockquote>", reply_markup=keyb)
    await message.delete()
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

# Поиск реферала
@dp.message_handler(state=states.search_ref.start)
async def ref_search(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()

    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username=?", (message.text,)).fetchone()

    if not user:
        msg = await message.answer(f"<blockquote><b>🔴 {message.text} не существует!</b></blockquote>", reply_markup=kb.back("refs"))
    else:
        if user[4] != message.from_user.id:
            msg = await message.answer(f"<blockquote><b>🔴 {message.text} не ваш реферал!</b></blockquote>", reply_markup=kb.back("refs"))
        else:
            msg = await message.answer(f"<blockquote><b>🟢 {message.text} ваш реферал!</b></blockquote>", reply_markup=kb.back("refs"))
    
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

# Управление пользователем
@dp.message_handler(state=states.ControlUser.start)
async def control_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()
    if message.text.isdigit():
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            user = cursor.execute("SELECT * FROM users WHERE id=?", (message.text,)).fetchone()
        if not user:
            msg = await message.answer("<blockquote><b>⚡️ Пользователь с таким ID не найден.</b></blockquote>", reply_markup=kb.back("control_user"))
        else:
            msg = await message.answer(f"<blockquote><b>⚡️ Пользователь {user[2]}</b></blockquote>", reply_markup=kb.control(user[0]))
    else:
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            user = cursor.execute("SELECT * FROM users WHERE username=?", (message.text,)).fetchone()
        if not user:
            msg = await message.answer("<blockquote><b>⚡️ Пользователь с таким username не найден.</b></blockquote>", reply_markup=kb.back("control_user"))
        else:
            msg = await message.answer(f"<blockquote><b>⚡️ Пользователь {user[2]}</b></blockquote>", reply_markup=kb.control(user[0]))
    
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

# Отправление сообщения пользователю
@dp.message_handler(state=states.SendMessage.start)
async def send_message_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    user_id = data.get('user_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()
    await bot.send_message(user_id, f"<blockquote><b>💌 Сообщение от администратора: <code>{message.text}</code></b></blockquote>")
    msg = await message.answer("<b>⚡️ Сообщение отправлено!</b>", reply_markup=kb.back(f"control_user:{user_id}"))
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

# Новая максимальная ставка
@dp.message_handler(state=states.ChangeMax.start)
async def change_max(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET max_amount=?", (message.text,))
        conn.commit()
    msg = await message.answer(f"<blockquote><b>⚡️ Максимальная сумма ставки была изменена на <code>{message.text}</code> $</b></blockquote>", reply_markup=kb.back("admin"))
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

# Установка нового счета
@dp.message_handler(state=states.ChangeInvoice.start)
async def change_invoice(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE settings SET invoice_link=?", (message.text,))
        conn.commit()
    msg = await message.answer(f"<blockquote><b>⚡️ Счет был изменен на <code>{message.text}</code></b></blockquote>", reply_markup=kb.back("admin"))
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

# Депозит
@dp.message_handler(state=states.Deposit.start)
async def deposit_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    await state.finish()
    try:
        summa = float(message.text)
        summa_text = f"{summa:.2f}"
        invoice = create_invoice(summa)
        keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("⚡️ Оплатить", url=invoice), InlineKeyboardButton("◀️ Назад", callback_data='popol'))
        msg = await message.answer(f"<blockquote><b>⚡️ Пополнение казны на сумму {summa_text}$</b></blockquote>", reply_markup=keyb)
    except:
        msg = await message.answer("<blockquote><b>⚡️ Отправляйте сумму числами! Повторите попытку еще раз!", reply_markup=kb.back("admin"))
    
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
        conn.commit()

    await message.delete()

@dp.message_handler(state=states.Broadcast.start)
async def broadcast_handler(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        data = await state.get_data()
        msg1_id = data.get('msg1_id')
        msg2_id = data.get('msg2_id')
        await bot.delete_message(message.chat.id, msg2_id)
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

            total_bets = cursor.execute("SELECT COUNT(*) FROM bets").fetchone()[0]
            total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets").fetchone()[0]
            if not total_bets_summ:
                    total_bets_summ = float(0.00)
            else:
                total_bets_summ = float(total_bets_summ)
                total_bets_summ = f"{total_bets_summ:.2f}"

            total_wins = cursor.execute("SELECT COUNT(*) FROM bets WHERE win=1").fetchone()[0]
            total_wins_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1").fetchone()[0]
            if not total_wins_summ:
                total_wins_summ = float(0.00)
            else:
                total_wins_summ = float(total_wins_summ)
                total_wins_summ = f"{total_wins_summ:.2f}"

            total_loses = cursor.execute("SELECT COUNT(*) FROM bets WHERE lose=1").fetchone()[0]
            total_loses_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE lose=1").fetchone()[0]
            if not total_loses_summ:
                total_loses_summ = float(0.00)
            else:
                total_loses_summ = float(total_loses_summ)
                total_loses_summ = f"{total_loses_summ:.2f}"

            msg = await bot.edit_message_text(f"<blockquote><b>⚡️ Админ-Панель\n├ Пользователей - <code>{total_users}</code> шт.\n├ Общее количество ставок - </b>~<b> <code>{total_bets}</code> шт. </b>[~ <code>{total_bets_summ}</code> <b>$</b>]\n<b>├ Выигрышей - </b>~<b> <code>{total_wins}</code> шт. </b>[~ <code>{total_wins_summ}</code> <b>$</b>]\n<b>└ Проигрышей - </b>~<b> <code>{total_loses}</code> шт. </b>[~ <code>{total_loses_summ}</code> <b>$</b>]</blockquote>", message.chat.id, msg1_id, reply_markup=kb.admin())
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
                conn.commit()
            await message.delete()
            return
    if message.text == "Я подтверждаю рассылку":
        data = await state.get_data()
        msg1_id = data.get('msg1_id')
        msg2_id = data.get('msg2_id')
        text = data.get('text')
        await bot.delete_message(message.chat.id, msg1_id)
        await bot.delete_message(message.chat.id, msg2_id)
        msg = await message.answer("<blockquote><b>⚡️ Идёт рассылка...</b></blockquote>")
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
            conn.commit()
        await message.delete()
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            users = cursor.execute("SELECT us_id FROM users").fetchall()
            failed = 0
            success = 0
            for user in users:
                try:
                    await bot.send_message(user[0], text)
                    success += 1
                except:
                    failed += 1
        msg = await msg.edit_text(f"<blockquote><b>⚡️ Рассылка завершена!\n\nОтправлено: <code>{success}</code> шт.\nНе отправлено: <code>{failed}</code> шт.</b></blockquote>", reply_markup=kb.back("admin"))
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (msg.message_id,message.from_user.id,))
            conn.commit()
        return
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    msg = await message.answer("""<blockquote><b>⚡️ Рассылка</b>

Вы уверены что хотите отправить данное сообщение? (Ниже пример что увидят юзеры)

<i>Для подтверждения напишите <code>Я подтверждаю рассылку</code> и для отмены напишите <code>Отмена</code></i></blockquote>""")
    msg2 = await message.answer(message.text, parse_mode="HTML")
    await state.update_data(msg1_id=msg.message_id)
    await state.update_data(msg2_id=msg2.message_id)
    await state.update_data(text=message.text)
    await message.delete()

# /vemorr
@dp.message_handler(commands='vemorr', state='*')
async def vemorr(message: types.Message, state: FSMContext):
    await state.finish()

    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        to_pay = cursor.execute("SELECT to_pay FROM vemorr").fetchone()[0]
        payed = cursor.execute("SELECT payed FROM vemorr").fetchone()[0]

    await message.answer(f"<b>✨ К выплате - {to_pay}$\n✨ Выплачено - {payed}$\n\n✨ Выплатить - @roleg</b>")

# /payed
@dp.message_handler(commands='payed', state='*')
async def payed(message: types.Message, state: FSMContext):
    if message.from_user.id == 640612893:
        await state.finish()

        args = message.get_args()
        if args:
            try:
                summa = float(args)

                with sqlite3.connect("db.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE vemorr SET payed=?, to_pay=to_pay-?", (summa,summa,))
                    conn.commit()
                    to_pay = cursor.execute("SELECT to_pay FROM vemorr").fetchone()[0]
                    if '-' in str(to_pay):
                        cursor.execute("UPDATE vemorr SET to_pay=0")
                        conn.commit()

                await message.answer("<b>✨ Done!</b>")
            except Exception as e:
                await message.answer("<b>✨ vem tu dayn?</b>")
        else:
            await message.answer("<b>✨ vem tu dayn?</b>")
    else:
        await message.delete()

# Колбэки
@dp.callback_query_handler(lambda call: True, state='*')
async def calls(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        exist = cursor.execute("SELECT * FROM users WHERE us_id=?", (call.from_user.id,)).fetchone()
        if not exist:
            cursor.execute("INSERT OR IGNORE INTO users(us_id,username) VALUES(?,?)", (call.from_user.id,call.from_user.mention,))
        else:
            cursor.execute("UPDATE users SET username=? WHERE us_id=?", (call.from_user.mention,call.from_user.id,))
        conn.commit()
    
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET msg_id=? WHERE us_id=?", (call.message.message_id,call.from_user.id,))
        conn.commit()

    check = await is_subscribed_to_channel(call.from_user.id, call.from_user.mention)

    if check:
        pass
    else:
        keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("⚡️ Подписаться", url=config.BETS_LINK))
        await call.message.edit_text("<blockquote><b>❌ Чтобы продолжить вы должны быть подписаными на канал ставок, после того как вы подписались пропишите заново /start</b></blockquote>", reply_markup=keyb)

    if call.data == 'profile':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            winning_bets = cursor.execute("SELECT COUNT(*) FROM bets WHERE win=1 AND us_id=?", (call.from_user.id,)).fetchone()[0]
            total_bets = cursor.execute("SELECT COUNT(*) FROM bets WHERE us_id=?", (call.from_user.id,)).fetchone()[0]
            total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE us_id=?", (call.from_user.id,)).fetchone()[0]
            if not total_bets_summ:
                total_bets_summ = float(0.00)
            else:
                total_bets_summ = float(total_bets_summ)
                total_bets_summ = f"{total_bets_summ:.2f}"
            join_date_str = cursor.execute("SELECT join_date FROM users WHERE us_id=?", (call.from_user.id,)).fetchone()[0]

        winrate = calculate_winrate(winning_bets, total_bets)
        winrate = f"{winrate:.2f}"
        join_date = datetime.strptime(join_date_str, "%Y-%m-%d %H:%M:%S")
        current_date = datetime.now()
        difference = current_date - join_date
        days_joined = difference.days
        days_joined_text = days_text(days_joined)
        formatted_date_str = join_date.strftime("%d.%m.%Y")

        await call.answer()
        await call.message.edit_text(f"""<blockquote><b>⚡️ Профиль {call.from_user.first_name}\n\nℹ️ Информация\n├ WinRate - <code>{winrate}%</code>\n├ Ставки за все время - <code>{total_bets_summ}$</code> за <code>{total_bets}</code> игр\n└ Дата регистрации - <code>{formatted_date_str}</code> </b>(<code>{days_joined_text}</code>)</blockquote>""", reply_markup=kb.profile())
    elif call.data == 'menu':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()

            total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE us_id=?", (call.from_user.id,)).fetchone()[0]
            if not total_bets_summ:
                total_bets_summ = float(0.00)
                total_bets_summ = f"{total_bets_summ:.2f}"
            else:
                total_bets_summ = float(total_bets_summ)
                total_bets_summ = f"{total_bets_summ:.2f}"
            
            total_wins_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1 AND us_id=?", (call.from_user.id,)).fetchone()[0]
            if not total_wins_summ:
                total_wins_summ = float(0.00)
                total_wins_summ = f"{total_wins_summ:.2f}"
            else:
                total_wins_summ = float(total_wins_summ)
                total_wins_summ = f"{total_wins_summ:.2f}"
            
            total_lose_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE lose=1 AND us_id=?", (call.from_user.id,)).fetchone()[0]
            if not total_lose_summ:
                total_lose_summ = float(0.00)
                total_lose_summ = f"{total_lose_summ:.2f}"
            else:
                total_lose_summ = float(total_lose_summ)
                total_lose_summ = f"{total_lose_summ:.2f}"

        await call.answer()
        await call.message.edit_text(f"<blockquote><b>👋 Добро пожаловать в реферального бота {config.CASINO_NAME}!\n\n🎲 Статистика ваших ставок\n├ Общая сумма ставок - {total_bets_summ}$\n├ Сумма выигрышей - {total_wins_summ}$\n└ Сумма проигрышей - {total_lose_summ}$</b></blockquote>", reply_markup=kb.menu(call.from_user.id))
    elif call.data == 'stats':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()

            total_games = cursor.execute("SELECT COUNT(*) FROM bets").fetchone()[0]
            total_payouts = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1").fetchone()[0]

            if not total_payouts:
                total_payouts = round(0.00)
            else:
                total_payouts = round(total_payouts)

            formatted_wins = f"{total_payouts:,}".replace(",", " ")
            total_rub = await convert(total_payouts)
            total_rub = round(total_rub)
            formatted_rub = f"{total_rub:,}".replace(",", " ")
        
        await call.answer()
        await call.message.edit_text(f"<blockquote><b>⚡️ Статистика о нашем проекте\n├ Общее количество игр - <code>{total_games}</code> шт.\n├ \n├ Сумма общих выплат:\n├ <code>{formatted_wins}$</code>\n└ <code>{formatted_rub}₽</code></b></blockquote>", reply_markup=kb.back("menu"))
    elif call.data == 'ref_panel':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            total_refs = cursor.execute("SELECT COUNT(*) FROM users WHERE ref=?", (call.from_user.id,)).fetchone()[0]
            ref_balance = cursor.execute("SELECT ref_balance FROM users WHERE us_id=?", (call.from_user.id,)).fetchone()[0]
            ref_balance = float(ref_balance)
            ref_balance = f"{ref_balance:.7f}"
        await call.answer()
        bot_username = await bot.get_me()
        await call.message.edit_text(f"<blockquote><b>⚡️ Реферальная панель\n├ Вы будете получать <code>10%</code> от проигрыша вашего реферала\n├ Вывод доступен от <code>0.2$</code>\n├ \n├ Количество рефералов - <code>{total_refs}</code> шт.\n├ Ваш реферальный баланс - <code>{ref_balance}$</code>\n└ Реф. Ссылка - <code>https://t.me/{bot_username.username}?start=ref_{call.from_user.id}</code></b></blockquote>", reply_markup=kb.ref())
    elif call.data == 'refs':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            refs = cursor.execute("SELECT * FROM users WHERE ref=?", (call.from_user.id,)).fetchall()

        per_page = 10
        total_pages = (len(refs) - 1) // per_page + 1
        btns = []

        def generate_keyboard1(page: int):
            start = (page - 1) * per_page
            end = start + per_page
            keyb = types.InlineKeyboardMarkup(row_width=2)
            keyb.add(types.InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='empty_button'))

            for ref in refs[start:end]:
                btns.append(types.InlineKeyboardButton(text=ref[6], callback_data=f'empty_button'))

            keyb.add(*btns)

            if page > 1:
                keyb.add(types.InlineKeyboardButton(text="◀️", callback_data=f'page_{page - 1}'))
            if page < total_pages:
                keyb.add(types.InlineKeyboardButton(text="▶️", callback_data=f'page_{page + 1}'))

            keyb.add(types.InlineKeyboardButton(text="🔍 Поиск", callback_data='search_refferals'), 
                   types.InlineKeyboardButton(text="◀️ Назад", callback_data='ref_panel'))

            return keyb

        page = 1
        keyb = generate_keyboard1(page)

        await call.answer()
        await call.message.edit_text(f"<blockquote><b>📄 Вы открыли страницу {page}/{total_pages}:</b></blockquote>", reply_markup=keyb)
    elif call.data.startswith('page_'):
        page = int(call.data.split('_')[1])
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            refs = cursor.execute("SELECT * FROM users WHERE ref=?", (call.from_user.id,)).fetchall()
        per_page = 10
        total_pages = (len(refs) - 1) // per_page + 1

        keyb = generate_keyboard(page, refs, total_pages, per_page)
        await call.message.edit_text(f"<blockquote><b>📄 Вы открыли страницу {page}/{total_pages}:</b></blockquote>", reply_markup=keyb)
    elif call.data == 'search_refferals':
        await state.finish()
        await call.message.edit_text("<blockquote><b>⚡️ Введите @username реферала:</b></blockquote>", reply_markup=kb.back("refs"))
        await states.search_ref.start.set()
        await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'cashback':
        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cashback = cursor.execute("SELECT cashback FROM users WHERE us_id=?", (call.from_user.id,)).fetchone()[0]
        await call.answer()
        await call.message.edit_text(f"<blockquote><b>⚡️ Панель кэшбек системы\n├ В случае проигрыша вы получаете <code>7.5%</code> от суммы ставки\n├ Вывод доступен от <code>0.2$</code>\n└ Кэшбек-счет - <code>{cashback:.7f}$</code></b></blockquote>", reply_markup=kb.cashback())
    elif call.data == 'admin':
        if call.from_user.id in config.ADMINS:
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                total_users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

                total_bets = cursor.execute("SELECT COUNT(*) FROM bets").fetchone()[0]
                total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets").fetchone()[0]
                if not total_bets_summ:
                    total_bets_summ = float(0.00)
                else:
                    total_bets_summ = float(total_bets_summ)
                    total_bets_summ = f"{total_bets_summ:.2f}"

                total_wins = cursor.execute("SELECT COUNT(*) FROM bets WHERE win=1").fetchone()[0]
                total_wins_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1").fetchone()[0]
                if not total_wins_summ:
                    total_wins_summ = float(0.00)
                else:
                    total_wins_summ = float(total_wins_summ)
                    total_wins_summ = f"{total_wins_summ:.2f}"

                total_loses = cursor.execute("SELECT COUNT(*) FROM bets WHERE lose=1").fetchone()[0]
                total_loses_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE lose=1").fetchone()[0]
                if not total_loses_summ:
                    total_loses_summ = float(0.00)
                else:
                    total_loses_summ = float(total_loses_summ)
                    total_loses_summ = f"{total_loses_summ:.2f}"

                await call.answer()
                await call.message.edit_text(f"<blockquote><b>⚡️ Админ-Панель\n├ Пользователей - <code>{total_users}</code> шт.\n├ Общее количество ставок - </b>~<b> <code>{total_bets}</code> шт. </b>[~ <code>{total_bets_summ}</code> <b>$</b>]\n<b>├ Выигрышей - </b>~<b> <code>{total_wins}</code> шт. </b>[~ <code>{total_wins_summ}</code> <b>$</b>]\n<b>└ Проигрышей - </b>~<b> <code>{total_loses}</code> шт. </b>[~ <code>{total_loses_summ}</code> <b>$</b>]</blockquote>", reply_markup=kb.admin())
    elif call.data.startswith("set_stop:"):
        if call.from_user.id in config.ADMINS:
            await call.answer()

            set_to = call.data.split(":")[1]
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE settings SET stop=?", (set_to,))
                conn.commit()

            if int(set_to) == 1:
                await bot.send_message(config.CHANNEL_ID, "<b>СТОП СТАВКИ!</b>")
            elif int(set_to) == 0:
                await bot.send_message(config.CHANNEL_ID, "<b>Играем дальше!</b>")

            try:
                await call.message.edit_reply_markup(reply_markup=kb.admin())
            except Exception as e:
                print(e)
    elif call.data == 'send_tutorial':
        if call.from_user.id in config.ADMINS:
            await call.answer()

            keyb = InlineKeyboardMarkup().add(InlineKeyboardButton("🎓 Пройти обучение", callback_data='tutorial:1'))
            await bot.send_message(config.CHANNEL_ID, """<b>❓ Не понимаешь как сделать ставку?
— Тогда прочти обучение!</b>

<blockquote><b>🎓 Мы написали пошаговое обучение «Как сделать ставку».</b></blockquote>

<b>👇 Прочитать его можно по кнопке снизу:</b>""", reply_markup=keyb)
    elif call.data.startswith('tutorial:'):
        await call.answer()
        page = call.data.split(":")[1]
        page = int(page)
        keyb = InlineKeyboardMarkup(row_width=2)
        try:
            if page == 1:
                keyb.add(InlineKeyboardButton("↪️ Дальше", callback_data='tutorial:2'))
                await bot.send_message(call.from_user.id, """<b>👋 Привет, давай расскажу как сделать ставку!
    
<blockquote>[💎] Для начала тебе нужно совершить депозит в бота @send если ты еще этого не сделал.</blockquote></b>""", reply_markup=keyb)
            elif page == 11:
                keyb.add(InlineKeyboardButton("↪️ Дальше", callback_data='tutorial:2'))
                await bot.edit_message_text("""<b>👋 Привет, давай расскажу как сделать ставку!

<blockquote>[💎] Для начала тебе нужно совершить депозит в бота @send если ты еще этого не сделал.</blockquote></b>""", call.from_user.id, call.message.message_id, reply_markup=keyb)
            elif page == 2:
                keyb.add(InlineKeyboardButton("↩️ Назад", callback_data='tutorial:11'), InlineKeyboardButton("↪️ Дальше", callback_data='tutorial:3'))
                await call.message.edit_text(f"""<b>📝 Теперь ты должен выбрать на что хочешь поставить!</b>
    
<blockquote><b>📚 Все игры ты можешь найти в нашем канале!</b>
    
<b><a href="{config.RULES_LINK}">*тык*</a></b></blockquote>""", reply_markup=keyb)
            elif page == 3:
                keyb.add(InlineKeyboardButton("↩️ Назад", callback_data='tutorial:2'), InlineKeyboardButton("↪️ Дальше", callback_data='tutorial:4'))
                await call.message.edit_text(f"""<b>📍 После выбора необходимо оплатить счёт тем самым создав ставку!</b>
    
<blockquote><b>💎 Переходишь на оплату счету ({config.BET_URL}) -> Вводишь сумму ставки в нужной валюте -> Добавляешь комментарий, а именно ставка которую ты выбрал (Например меньше) -> Нажимаешь оплатить счет и наблюдаешь над ставкой в канале ставок.</b></blockquote>
    
<b>✅ Вот и всё! Если у вас возникли вопросы обратитесь к ТП.</b>""", reply_markup=keyb, disable_web_page_preview=True)
            elif page == 4:
                keyb.add(InlineKeyboardButton("↩️ Назад", callback_data='tutorial:3'))
                await call.message.edit_text(f"""<b>❓ Куда же приходит выплата в случае выигрыша?</b>
    
<blockquote><b>💹 Если вы выиграли то на ваш счёт @send моментально должны прийти средства.</b></blockquote>


<b>🛂 В случае проблем с зачислением средств на ваш счёт обратитесь к администратору (<a href="{config.OWNER_LINK}">*тык*</a>)</b>""", reply_markup=keyb, disable_web_page_preview=True)
        except:
            await call.answer("Вы должны быть в нашем реферальном боте!", show_alert=True)
    elif call.data == 'control_user':
        if call.from_user.id in config.ADMINS:
            await call.answer()
            await call.message.edit_text("<blockquote><b>⚡️ Отправьте @username или ID пользователя:</b></blockquote>", reply_markup=kb.back("admin"))
            await states.ControlUser.start.set()
            await state.update_data(msg_id=call.message.message_id)
    elif call.data.startswith("control_user:"):
        if call.from_user.id in config.ADMINS:
            userid = call.data.split(":")[1]
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                user = cursor.execute("SELECT * FROM users WHERE us_id=?", (userid,)).fetchone()
            await call.answer()
            await call.message.edit_text(f"<blockquote><b>⚡️ Пользователь {user[2]}</b></blockquote>", reply_markup=kb.control(user[0]))
    elif call.data.startswith("empty_ref:"):
        if call.from_user.id in config.ADMINS:
            userid = call.data.split(":")[1]
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET ref_balance=0 WHERE us_id=?", (userid,))
                conn.commit()
            await call.answer("Анулирован!", show_alert=True)
    elif call.data.startswith("empty_cashback:"):
        if call.from_user.id in config.ADMINS:
            userid = call.data.split(":")[1]
            with sqlite3.connect("db.db") as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET cashback=0 WHERE us_id=?", (userid,))
                conn.commit()
            await call.answer("Анулирован!", show_alert=True)
    elif call.data.startswith("send_message:"):
        if call.from_user.id in config.ADMINS:
            userid = call.data.split(":")[1]
            await call.answer()
            await call.message.edit_text("<blockquote><b>⚡️ Введите текст который хотите отправить пользователю:</b></blockquote>", reply_markup=kb.back(f"control_user:{userid}"))
            await states.SendMessage.start.set()
            await state.update_data(user_id=userid)
            await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'change_max':
        if call.from_user.id in config.ADMINS:
            await call.answer()
            await call.message.edit_text("<blockquote><b>⚡️ Введите новую сумму максимальной ставки:</b></blockquote>", reply_markup=kb.back("admin"))
            await states.ChangeMax.start.set()
            await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'change_invoice':
        if call.from_user.id in config.ADMINS:
            await call.answer()
            await call.message.edit_text("<blockquote><b>⚡️ Введите новую ссылку на счет:</b></blockquote>", reply_markup=kb.back("admin"))
            await states.ChangeInvoice.start.set()
            await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'popol':
        if call.from_user.id in config.ADMINS:
            await call.answer()
            balance = get_cb_balance()
            balance = float(balance)
            balance2 = max(balance - 0.01, 0)
            await call.message.edit_text(f"<blockquote><b>⚡️ Введите сумму на которую хотите пополнить казну:</b>\n\n<b>⚡️ Текущий баланс: <code>{balance}</code> USDT </b>[~ <code>{balance2}</code> <b>$</b>]</blockquote>", reply_markup=kb.back("admin"))
            await states.Deposit.start.set()
            await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'broadcast':
        if call.from_user.id in config.ADMINS:
            await call.answer()
            await call.message.edit_text("<blockquote><b>⚡️ Введите текст для рассылки</b></blockquote>", reply_markup=kb.back("admin"))
            await states.Broadcast.start.set()
            await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'statistics':
        if call.from_user.id in config.ADMINS:
            await call.answer()

            users = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            total_bets = cursor.execute("SELECT COUNT(*) FROM bets").fetchone()[0]
            total_bets_summ = cursor.execute("SELECT SUM(summa) FROM bets").fetchone()[0]

            if total_bets_summ:
                total_bets_summ = float(total_bets_summ)
            else:
                total_bets_summ = float(0)

            total_bets_summ = f"{total_bets_summ:.2f}"
            total_wins = cursor.execute("SELECT COUNT(*) FROM bets WHERE win=1").fetchone()[0]
            total_wins_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE win=1").fetchone()[0]

            if total_wins_summ:
                total_wins_summ = float(total_wins_summ)
            else:
                total_wins_summ = float(0)

            total_wins_summ = f"{total_wins_summ:.2f}"
            total_loses = cursor.execute("SELECT COUNT(*) FROM bets WHERE lose=1").fetchone()[0]
            total_loses_summ = cursor.execute("SELECT SUM(summa) FROM bets WHERE lose=1").fetchone()[0]

            if total_loses_summ:
                total_loses_summ = float(total_loses_summ)
            else:
                total_loses_summ = float(0)

            total_loses_summ = f"{total_loses_summ:.2f}"

            await call.message.edit_text(f"<blockquote><b>⚡️ Статистика бота</b>\n\n<i>Пользователей в боте - <code>{users}</code> <b>шт.</b>\nВсего ставок - <code>{total_bets}</code> <b>шт.</b> [~ <code>{total_bets_summ}</code> <b>$</b>]\nВыигрышей - <code>{total_wins}</code> <b>шт.</b> [~ <code>{total_wins_summ}</code> <b>$</b>]\nПроигрышей - <code>{total_loses}</code> <b>шт.</b> [~ <code>{total_loses_summ}</code> <b>$</b>]</i></blockquote>", reply_markup=kb.back("admin"))
    elif call.data == 'checks':
        await call.answer()
        headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
        r = requests.get("https://pay.crypt.bot/api/getChecks", headers=headers).json()
        keyb = InlineKeyboardMarkup(row_width=2)
        btns = []
        if r['ok'] == True:
            items = r['result']['items']
            for item in items:

                check_id = item['check_id']

                status = None
                if item['status'] == 'activated':
                    pass
                elif item['status'] == 'active':
                    status = '❌'
                else:
                    status = '❓'

                if status == None:
                    pass
                else:
                    btns.append(InlineKeyboardButton(f"{status}. {item['amount']} {item['asset']}", callback_data=f'check:{check_id}'))
            keyb.add(*btns)
        else:
            keyb.add(InlineKeyboardButton("❌ Произошла ошибка.", callback_data='empty'))
        keyb.add(InlineKeyboardButton("◀️ Назад", callback_data='admin'))

        await call.message.edit_text("<blockquote><b>⚡️ Управление чеками</b></blockquote>", reply_markup=keyb)
    elif call.data.startswith("check:"):
        await call.answer()
        check_id = call.data.split(":")[1]
        headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
        data = {"check_ids": check_id}
        r = requests.get("https://pay.crypt.bot/api/getChecks", headers=headers, data=data).json()
        keyb = InlineKeyboardMarkup(row_width=1)
        if r['ok'] == True:
            items = r['result']['items']
            for item in items:

                if str(item['check_id']) == str(check_id):

                    pinned_to = item['pin_to_user']['user_id']

                    if item['status'] == 'activated':
                        status = 'Активирован'
                    elif item['status'] == 'active':
                        status = 'Не активирован'
                    else:
                        status = 'Неизвестно'

                    summa = f"{item['amount']} {item['asset']}"
                    check_id = item['check_id']

                    keyb.add(InlineKeyboardButton("⚡️ Удалить чек", callback_data=f'delete_check:{check_id}'))
                    keyb.add(InlineKeyboardButton("◀️ Назад", callback_data='admin'))
                    await call.message.edit_text(
                        f"<blockquote><b>⚡️ Управление чеком\n\nЗакреплен за - {pinned_to}\nСтатус - {status}\nСумма - {summa}</b></blockquote>",
                        reply_markup=keyb)
                    return
        else:
            pinned_to = 'Неизвестно'
            status = 'Неизвестно'
            summa = 'Неизвестно'
            keyb.add(InlineKeyboardButton("❌ Произошла ошибка.", callback_data='empty'))
            keyb.add(InlineKeyboardButton("◀️ Назад", callback_data='admin'))

            await call.message.edit_text(f"<blockquote><b>⚡️ Управление чеком\n\nЗакреплен за - {pinned_to}\nСтатус - {status}\nСумма - {summa}</b></blockquote>", reply_markup=keyb)
            return
    elif call.data.startswith("delete_check:"):
        check_id = call.data.split(":")[1]
        headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
        data = {"check_id": check_id}
        r = requests.post("https://pay.crypt.bot/api/deleteCheck", headers=headers, data=data).json()
        if r['ok'] == True:
            await call.answer("Чек удален!", show_alert=True)
            headers = {"Crypto-Pay-API-Token": config.CRYPTOPAY_TOKEN}
            r = requests.get("https://pay.crypt.bot/api/getChecks", headers=headers).json()
            keyb = InlineKeyboardMarkup(row_width=2)
            btns = []
            if r['ok'] == True:
                items = r['result']['items']
                for item in items:

                    status = None
                    if item['status'] == 'activated':
                        pass
                    elif item['status'] == 'active':
                        status = '❌'
                    else:
                        status = '❓'
                    
                    check_id = item['check_id']

                    if status == None:
                        pass
                    else:
                        btns.append(InlineKeyboardButton(f"{status}. {item['amount']} {item['asset']}", callback_data=f'check:{check_id}'))
                keyb.add(*btns)
            else:
                keyb.add(InlineKeyboardButton("❌ Произошла ошибка.", callback_data='empty'))
            keyb.add(InlineKeyboardButton("◀️ Назад", callback_data='admin'))

            await call.message.edit_text("<blockquote><b>⚡️ Управление чеками</b></blockquote>", reply_markup=keyb)
        else:
            await call.answer("Ошибка удаления чека!", show_alert=True)
    elif call.data == 'withdraw':
        await call.message.edit_text("<blockquote><b>⚡️ Введите сумму которую вы хотите вывести, от 0.2$</b></blockquote>", reply_markup=kb.back("admin"))
        await states.Withdraw.start.set()
        await state.update_data(msg_id=call.message.message_id)
    elif call.data == 'links':
        await call.answer("Временно не работает.", show_alert=True)
    else:
        await call.answer()

# Вывод казны
@dp.message_handler(state=states.Withdraw.start)
async def withdraw_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    await bot.delete_message(message.chat.id, msg_id)
    try:
        summa = float(message.text)
        if summa < float(0.2):
            await message.answer("<blockquote><b>❌ Сумма меньше 0.2$!</b></blockquote>", reply_markup=kb.back("admin"))
            await message.delete()
            return
        else:
            cb_balance = get_cb_balance()
            if float(cb_balance) < summa:
                await message.answer("<blockquote><b>❌ В казне не достаточно средств!</b></blockquote>", reply_markup=kb.back("admin"))
                await message.delete()
                return
            else:
                if summa >= float(1.2):
                    await state.finish()
                    await transfer(summa, message.from_user.id)
                    await message.answer("<blockquote><b>⚡️ Средства были выведены на ваш счет!</b></blockquote>", reply_markup=kb.back("admin"))
                    await message.delete()
                    return
                elif summa >= float(0.2):
                    await state.finish()
                    check = await create_check(summa, message.from_user.id)
                    keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Забрать средства", url=check), InlineKeyboardButton("◀️ Назад", callback_data='admin'))
                    await message.answer("<blockquote><b>⚡️ Успешно! Заберите чек ниже</b></blockquote>", reply_markup=keyb)
                    await message.delete()
                    return
                else:
                    await message.answer("<blockquote><b>❌ Неизвестная ошибка!</b></blockquote>", reply_markup=kb.back("admin"))
                    await message.delete()
                    return
    except:
        await message.answer("<blockquote><b>❌ Вводить сумму надо числами!</b></blockquote>", reply_markup=kb.back("admin"))
        await message.delete()
        return

# Неизвестная команда
@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.delete()

# Сам код твоего бота измененный мною
# Надежный способ получения через entities ниже

# Надежный способ получения через entities ниже
def parse_message(message: types.Message):
 if message.entities:
    if message.entities[0].user:
        user = message.entities[0].user
        name = user.full_name
        msg_text = message.text.removeprefix(name).replace("🪙", "")
        user_id = int(user.id)
        asset = msg_text.split("отправил(а)")[1].split()[1]
        amount = float(msg_text.split("отправил(а)")[1].split()[0].replace(',', ""))

        if '💬' in message.text:
            comment = message.text.split("💬 ")[1].lower()
            game = comment.replace("ё", "е").replace("ное", "").replace(" ", "").replace("куб", "")
        else:
            comment = None
            game = None

        return {
            'id': user_id,
            'name': name,
            'usd_amount': amount,
            'asset': asset,
            'comment': comment,
            'game': game
        }

def create_keyboard(check=None, summa=None):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if check == None and summa == None:
        bet_button = InlineKeyboardButton("Сделать ставку", url=config.BET_URL)        
        keyboard.add(bet_button)
    else:
        claim_check = InlineKeyboardButton(f"🎁 Забрать {summa:.2f}$", url=check)
        bet_button = InlineKeyboardButton("Сделать ставку", url=config.BET_URL)
        keyboard.row(claim_check)        
        keyboard.row(bet_button)
    return keyboard

async def send_result_message(result, parsed_data, dice_result, coefficient, us_id, msg_id):
    emoji, winning_values = DICE_CONFIG[parsed_data['comment']]
    bot_username = await bot.get_me()
    bot_username = bot_username.username

    if 'камень' in parsed_data['comment'] or 'ножницы' in parsed_data['comment'] or 'бумага' in parsed_data['comment']:
        choose = ['✋', '👊', '✌️']
        choice = random.choice(choose)
        await asyncio.sleep(1)
        msg_dice = await bot.send_message(config.CHANNEL_ID, text=choice, reply_to_message_id=msg_id)
        dice_value = msg_dice.text
        result = dice_value in winning_values
        if result:
            result = True
        elif not result:
            result = False
        else:
            result = False
    
    if 'победа 1' in parsed_data['comment'] or 'п1' in parsed_data['comment'] or 'победа 2' in parsed_data['comment'] or 'п2' in parsed_data['comment'] or 'ничья' in parsed_data['comment']:
        dice1 = dice_result
        dice2 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
        dice2 = dice2.dice.value

        if dice1 > dice2:
            if 'победа 1' in parsed_data['comment'] or 'п1' in parsed_data['comment']:
                result = True
            else:
                result = False
        elif dice1 < dice2:
            if 'победа 2' in parsed_data['comment'] or 'п2' in parsed_data['comment']:
                result = True
            else:
                result = False
        elif dice1 == dice2:
            if 'ничья' in parsed_data['comment']:
                result = True
            else:
                result = False

    if 'пвп' in parsed_data['comment']:
        dice1 = dice_result
        dice2 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
        dice2 = dice2.dice.value
        await bot.send_message(config.CHANNEL_ID, "<b>♻️ Отправляет бот...</b>")
        bot_dice1 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
        bot_dice1 = bot_dice1.dice.value
        bot_dice2 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
        bot_dice2 = bot_dice2.dice.value

        player = dice1 + dice2
        bot_result = bot_dice1 + bot_dice2

        if player > bot_result:
            result = True
        elif player < bot_result:
            result = False
        elif player == bot_result:
            await bot.send_message(config.CHANNEL_ID, "<b>♻️ Ничья, кидаю кубики заново.</b>")
            await send_result_message(result=None, parsed_data=parsed_data, dice_result=dice_result, coefficient=coefficient, us_id=us_id, msg_id=msg_id)
            return

    if result:
        usd_amount = parsed_data['usd_amount']
        usd_amount = float(usd_amount)
        minus_cashback = usd_amount * (7.5 / 100)

        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO bets(us_id, summa, win) VALUES(?, ?, 1)", (parsed_data['id'], usd_amount,))
            cursor.execute("UPDATE users SET cashback=cashback-? WHERE us_id=?", (minus_cashback, parsed_data['id'],))
            conn.commit()
            user = cursor.execute("SELECT cashback FROM users WHERE us_id=?", (parsed_data['id'],)).fetchone()[0]
            if float(user) < float(0):
                cursor.execute("UPDATE users SET cashback=0.0 WHERE us_id=?", (parsed_data['id'],))
                conn.commit()

        if 'плинко' in parsed_data['comment']:
            if dice_result == 4:
                winning_amount_usd = float(parsed_data['usd_amount'] * 1.1)
            elif dice_result == 5:
                winning_amount_usd = float(parsed_data['usd_amount'] * 1.5)
            elif dice_result == 6:
                winning_amount_usd = float(parsed_data['usd_amount'] * 1.95)
        else:
            winning_amount_usd = float(parsed_data['usd_amount']) * coefficient

        cb_balance = get_cb_balance()
        cb_balance = float(cb_balance)
        if cb_balance < winning_amount_usd:
            keyb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💼 Перейти к пользователю", url=f"tg://user?id={us_id}"))
            await bot.send_message(config.LOGS_ID, f"<b>[🔔] Мало суммы в казне для выплаты!</b>\n\n<b><blockquote>Пользователь: {us_id}\nСумма: {winning_amount_usd}$</blockquote></b>", reply_markup=keyb)
            keyboard = create_keyboard()
            result_message = (
                f"<b> Поздравляем, вы выиграли</b>\n\n"
                f"<blockquote><i>Победитель получит</i> <b>{winning_amount_usd:.2f}$</b> <i>администрацией вручную</i></blockquote>\n\n"
                f"<blockquote>Ставь ставку и испытывай удачу!</blockquote>\n\n"
                f"<b><a href='{config.RULES_LINK}'>Как сделать ставку?</a> | <a href='{config.NEWS_LINK}'>Новостной канал</a> | <a href='https://t.me/{bot_username}'>Реферальный бот</a></b>"
            )
        else:
            if winning_amount_usd >= 1.12:
                await transfer(winning_amount_usd, us_id)
                keyboard = create_keyboard()
                result_message = (
                    f"<b> Поздравляем, вы выиграли</b>\n\n"
                    f"<blockquote><b>Победитель получил {winning_amount_usd:.2f}$</blockquote>\n\n"
                    f"<blockquote>Ставь ставку и испытывай удачу!</blockquote>\n\n"
                    f"<b><a href='{config.RULES_LINK}'>Как сделать ставку?</a> | <a href='{config.NEWS_LINK}'>Новостной канал</a> | <a href='https://t.me/{bot_username}'>Реферальный бот</a></b>"
                )
            else:
                check = await create_check(winning_amount_usd, us_id)
                keyboard = create_keyboard(check, winning_amount_usd)
                result_message = (
                    f"<b> Поздравляем, вы выиграли</b>\n\n"
                    f"<blockquote><b>Заберите свои {winning_amount_usd:.2f}$ кнопкой ниже</blockquote>\n\n"
                    f"<blockquote>Ставь ставку и испытывай удачу!</blockquote>\n\n"
                    f"<b><a href='{config.RULES_LINK}'>Как сделать ставку?</a> | <a href='{config.NEWS_LINK}'>Новостной канал</a> | <a href='https://t.me/{bot_username}'>Реферальный бот</a></b>"
                )
    else:
        usd_amount = parsed_data['usd_amount']
        usd_amount = float(usd_amount)
        add_cashback = usd_amount * (7.5 / 100)
        add_ref = usd_amount * (10 / 100)
        to_vemorr = usd_amount * (10 / 100)

        with sqlite3.connect("db.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE vemorr SET to_pay=to_pay+?", (to_vemorr,))
            cursor.execute("INSERT INTO bets(us_id,summa,lose) VALUES(?,?,1)", (parsed_data['id'],usd_amount,))
            cursor.execute("UPDATE users SET cashback=cashback+? WHERE us_id=?", (add_cashback,parsed_data['id'],))
            conn.commit()
            ref = cursor.execute("SELECT ref FROM users WHERE us_id=?", (parsed_data['id'],)).fetchone()[0]
            if not ref:
                pass
            else:
                cursor.execute("UPDATE users SET ref_balance=ref_balance+? WHERE us_id=?", (add_ref,ref,))
                conn.commit()
                await bot.send_message(ref, f"<blockquote><b>⚡️ Выплата с реферала!</b>\n\n<b>⚡️ +{add_ref}$ на реферальный баланс!</b></blockquote>")

        keyboard = create_keyboard()
        result_message = (
            f"<b>Проигрыш</b>\n\n"
            f"<blockquote><b>Не удачная ставка, сделай ставку ещё раз чтобы испытать удачу сполна!</b></blockquote>\n\n"            
            f"<blockquote><i>Кешбек в размере {add_cashback:.2f}$  зачислен на ваш кешбек баланс</i></blockquote>\n\n"
            f"<b><a href='{config.RULES_LINK}'>Как сделать ставку?</a> | <a href='{config.NEWS_LINK}'>Новостной канал</a> | <a href='https://t.me/{bot_username}'>Реферальный бот</a></b>"
        )

    return result_message, keyboard

async def handle_bet(parsed_data, bet_type, us_id, msg_id, oplata_id, processed_lines, line):
    try:
        emoji, winning_values = DICE_CONFIG[bet_type]
        if emoji and winning_values or emoji or winning_values:
            if 'зеро' in parsed_data['comment'] or 'черное' in parsed_data['comment'] or 'красное' in parsed_data['comment']:
                roulette = ['CAACAgIAAxkBAAEMc65miwstwNiEg2zA8AJbzcIRFqMC1wACa0wAAoogUEqSy15B1lxZkTUE', 'CAACAgIAAxkBAAEsaY9miwmyqrlOY0BuUad3fwVMovJiFAACq1AAAsg8WUraWoiatb18GDUE', 'CAACAgIAAxkBAAEMc7Bmiwsw5IM2WLQueYYdK2HXwMXHgwACa04AAusJUEpRWiMnFgPASzUE', 'CAACAgIAAxkBAAEMc2ZmiwnilFhFhr4mNCSRhAM7T6ypxAACFksAAj60UEo229Tfsbc5QjUE', 'CAACAgIAAxkBAAEMc2hmiwnobjZAWgpFjo8CBuc0Ob1eewACxk0AAvLaUUpl9jec4WWwkjUE', 'CAACAgIAAxkBAAEMc2pmiwn2Q17M172AVXzMYrhjHrZQ_wACy1AAAjj_UUrCBC92XVbpfDUE', 'CAACAgIAAxkBAAEMc2xmiwn6jEqaRsN2FIIY-gitGpl_-wAC0kUAAlEuWUoAAeD330H2Uo01BA', 'CAACAgIAAxkBAAEMc25miwn7S46y-CsODDYAAZBtodp7VA8AAo9PAALASFBKN_ZkjOauQfQ1BA', 'CAACAgIAAxkBAAEMc3Bmiwn8mqlAxeREXIxb0hn8LZIVCQACiUEAAkhJWUoHGtNoD3zTsDUE', 'CAACAgIAAxkBAAEMc3Jmiwn-LB86peNFQGOfHNWA-nRXDAAC5VEAAkrJUUqgM9OL3fCB2TUE', 'CAACAgIAAxkBAAEMc3Rmiwn_zG0H3WAxQheAorM4_4NaowACgEAAAknlWEq8GP_mPFMm3TUE', 'CAACAgIAAxkBAAEMc3ZmiwoAAf47DgvUQCP32yvbfeBJjuMAAvJAAAIj0llKg0CyCQnMOLE1BA', 'CAACAgIAAxkBAAEMc3dmiwoCxxFrMcJSWMR2033giZzijwACLEcAAlrbWUoi1YY6EOFq9zUE', 'CAACAgIAAxkBAAEMc3pmiwoDxKPt9r_zGsRcHqNy22dmlAACw1EAAv0eWEqm1mam-L-5JTUE', 'CAACAgIAAxkBAAEMc3xmiwoEIrD5q_nHBhjks3Evx7D7iwAChT8AAmaFWEqEpRMkssTyhzUE', 'CAACAgIAAxkBAAEMc35miwoFoJFbsigX7aEExD5mLwh24AACoEcAAl5EWUqVzM66FWlaaDUE', 'CAACAgIAAxkBAAEMc4BmiwoHltn8IOBiRt5_5kePFVJpkgACeUUAAkyFWEoBVKx02Trj-DUE', 'CAACAgIAAxkBAAEMc4FmiwoIw6On42sEqgT8-QOXkk2MzwACgkwAAtR4WUqSD7f4umsywzUE', 'CAACAgIAAxkBAAEMc4RmiwoJmQPqnHX8Esl8bAxaI1IS2AACSE8AAoPtUUqiMruDVUZ1SDUE', 'CAACAgIAAxkBAAEMc4ZmiwoLoOEnZ-_cbcTme4b7crH4ZAACEkUAAhS9WEq7zrdRmpKo1TUE', 'CAACAgIAAxkBAAEMc4hmiwoNtSwKZRbmQ8yXG0BPuSRLSgACvUwAA-FRSlhShWr5KKbXNQQ', 'CAACAgIAAxkBAAEMc4pmiwoOdPCN_UOzywpNf4W8eAfy8QACvVUAAmRIWUpdaTruYoIiRzUE', 'CAACAgIAAxkBAAEMc4xmiwoPgz770vyKhZrxCbOahEOd_wACz0UAAjV4WEr_1EXGVH2xoTUE', 'CAACAgIAAxkBAAEMc41miwoQUY0nnRVhOlCZQER4q9zycAACVE8AAkFDUErPxTJG2opUpDUE', 'CAACAgIAAxkBAAEMc49miwoRxoTw08HNuntIkmUYnU-dGgAC600AAobmWEooNhEix_a6mDUE', 'CAACAgIAAxkBAAEMc5JmiwoTrPP9CCjVu41kJqJrLAHXUgACiUwAAj83WEoxbzqmdO_2BzUE', 'CAACAgIAAxkBAAEMc5RmiwoV2vYbGQSRdtcQA7iioruU9gAC00AAAuweWEpbjeobSqzftDUE', 'CAACAgIAAxkBAAEMc5ZmiwoW0tlVbEAi7t3GAS_xGYyx4QACU0IAAj9nWErmrudsEouYuzUE', 'CAACAgIAAxkBAAEMc5dmiwoXpBYb5-hRQqnj-FCv4Mg81gACrGMAAquXWUp00Cv45-WZzjUE', 'CAACAgIAAxkBAAEMc5lmiwoYE7tDV_2F2LbCWt8yFRpN_wAC6EEAAid_WUp7iVzaYV8_AzUE', 'CAACAgIAAxkBAAEMc5tmiwoZxhdcG8kRbk25VilTjjCfqAAC4VIAAoEtWEr0-v_e-Xk48zUE', 'CAACAgIAAxkBAAEMc51miwoa5ESLXeX18fSNbK_D9XvIVAAC8VMAAjzjWEoJpnR_Gp2vRzUE', 'CAACAgIAAxkBAAEMc59miwocJwaSdr3K3H3pMqpVQ5gatQAC2UQAAvmlWUqjIfPUbYdAMzUE', 'CAACAgIAAxkBAAEMc6Jmiwoeqq5SjFcm5zrFHZlfoxGLigAC-UYAAulWWEphBgerbGYOITUE', 'CAACAgIAAxkBAAEMc6Rmiwogd-OhH8ireO4UExYkTAfw8QACtE8AAmMwUUoYWzy8PvnZJTUE', 'CAACAgIAAxkBAAEMc6Zmiwoh_UfUM2NzvJBFh0tIhRdcZAACpUsAAp0pWUrIAAEyPwZzvzk1BA', 'CAACAgIAAxkBAAEMc6dmiwoi131vko92X8XNEGROy7AYNgACMEYAAnEeWErMXjdnKkjeeTUE']
                choice = random.choice(roulette)
                choice = str(choice)
                await bot.send_sticker(config.CHANNEL_ID, sticker=choice, reply_to_message_id=msg_id)
                dice_result = choice
                result = dice_result in winning_values
                result_message, keyboard = await send_result_message(result, parsed_data, dice_result, COEFFICIENTS[bet_type], us_id, msg_id)
            elif 'камень' in parsed_data['comment'] or 'ножницы' in parsed_data['comment'] or 'бумага' in parsed_data['comment']:
                dice_message = await bot.send_message(config.CHANNEL_ID, text=emoji, reply_to_message_id=msg_id)
                dice_result = dice_message.text
                result = None
                result_message, keyboard = await send_result_message(result, parsed_data, dice_result, COEFFICIENTS[bet_type], us_id, msg_id)
            elif 'победа 1' in parsed_data['comment'] or 'п1' in parsed_data['comment'] or 'победа 2' in parsed_data['comment'] or 'п2' in parsed_data['comment'] or 'ничья' in parsed_data['comment']:
                dice1 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
                dice_result = dice1.dice.value
                result = None
                result_message, keyboard = await send_result_message(result, parsed_data, dice_result, COEFFICIENTS[bet_type], us_id, msg_id)
            elif 'пвп' in parsed_data['comment']:
                dice1 = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id)
                dice_result = dice1.dice.value
                result = None
                result_message, keyboard = await send_result_message(result, parsed_data, dice_result, COEFFICIENTS[bet_type], us_id, msg_id)
            else:
                dice_message = await bot.send_dice(config.CHANNEL_ID, emoji=emoji, reply_to_message_id=msg_id) if emoji else await bot.send_dice(config.CHANNEL_ID, reply_to_message_id=msg_id)
                dice_result = dice_message.dice.value
                result = dice_result in winning_values
                result_message, keyboard = await send_result_message(result, parsed_data, dice_result, COEFFICIENTS[bet_type], us_id, msg_id)
            await asyncio.sleep(4)
            result = '🔥 Победа!' if 'вы выиграли' in result_message else '❌ Проигрыш!'
            image = config.WIN_IMAGE if 'вы выиграли' in result_message else config.LOSE_IMAGE
            keyb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("💼 Перейти к пользователю", url=f"tg://user?id={us_id}"))
            await bot.send_message(config.LOGS_ID, f"""<blockquote><b>🎲 Исход ставки: <span class="tg-spoiler">{result}</span></b></blockquote>""", reply_markup=keyb, reply_to_message_id=oplata_id)
            await bot.send_photo(config.CHANNEL_ID, open(image, 'rb'), result_message, reply_markup=keyboard, reply_to_message_id=msg_id)
        else:
            amount = float(parsed_data['usd_amount'])
            summa = amount * (85 / 100)
            if float(cb_balance) >= float(summa) and float(summa) >= 0.02:
                check = await create_check(summa, user_id)
                await bot.send_message(config.CHANNEL_ID, f"<blockquote><b> {parsed_data['name']} - Вы</b><i> забыли дописать комментарий к ставке или написали его не верно</i></blockquote>\n\n<i>Был совершён возврат денежных средств с комиссией 15%</i>", reply_markup=create_keyboard(check, summa))
            else:
                check = await create_check(summa, user_id)
                await bot.send_message(config.CHANNEL_ID,
                                       f"<blockquote><b>❌ {parsed_data['name']}, вы указали не верный комментарий к платежу!</b>\n\n</blockquote>\n\n<i>Был совершён возврат денежных средств с комиссией 15%</i>\n<b>Заберите ваши деньги у</b> <i>администратора</i>",
                                       reply_markup=create_keyboard())
    except Exception as e:
        await bot.send_message(config.LOGS_ID, f"<blockquote><b>❌ Ошибка при обработке ставки: <code>{str(e)}</code></b></blockquote>")

    processed_lines.append(line)

queue_file = 'bet_queue.txt'
processing_lock = asyncio.Lock()

async def add_bet_to_queue(user_id, username, amount, comment, msg_id):
    with open(queue_file, 'a', encoding='utf-8') as file:
        file.write(f"{user_id}‎ {username}‎ {amount}‎ {comment}‎ {msg_id}\n")

@dp.channel_post_handler()
async def check_messages(message: types.Message):
    try:
        if message.chat.id == config.LOGS_ID:
            if 'отправил(а)' in message.text:
                try:
                    async with processing_lock:

                        parsed_data = parse_message(message)

                        try:
                            with sqlite3.connect("db.db") as conn:
                                cursor = conn.cursor()
                                exist = cursor.execute("SELECT * FROM users WHERE us_id=?", (parsed_data['id'],)).fetchone()
                                if not exist:
                                    cursor.execute("INSERT OR IGNORE INTO users(us_id) VALUES(?)", (parsed_data['id'],))
                                    conn.commit()

                            with sqlite3.connect("db.db") as conn:
                                cursor = conn.cursor()
                                cursor.execute("INSERT INTO deposits(us_id,summa) VALUES(?,?)", (parsed_data['id'],parsed_data['usd_amount'],))
                                conn.commit()
                        except:
                            pass

                        name = parsed_data['name']
                        if "*" in name:
                            name = name.split("*")[0]

                        if '💬' in message.text:
                            await add_bet_to_queue(parsed_data['id'], name, parsed_data['usd_amount'], parsed_data['comment'], message.message_id)
                            await asyncio.sleep(1)
                        else:
                            await add_bet_to_queue(parsed_data['id'], name, parsed_data['usd_amount'], '', message.message_id)
                            await asyncio.sleep(1)

                        if os.path.exists(queue_file):
                            with open(queue_file, 'r', encoding='utf-8') as file:
                                lines = file.readlines()

                            processed_lines = []
                            for line in lines:

                                with sqlite3.connect("db.db") as conn:
                                    cursor = conn.cursor()
                                    status = cursor.execute("SELECT stop FROM settings").fetchone()[0]

                                if int(status) == 1:
                                    return

                                parts = line.strip().split('‎ ')
                                if len(parts) != 5:
                                    continue

                                user_id, username, amount, comment_lower, msg_id = parts

                                if user_id.isdigit():
                                    amount = float(amount)
                                    amount = f"{amount:.2f}"
                                    amount = float(amount)
                                    if not comment_lower or not comment_lower.strip() or comment_lower == '':
                                        summa = amount * (85 / 100)
                                        cb_balance = get_cb_balance()
                                        if float(cb_balance) >= float(summa) and float(summa) >= 0.02:
                                            check = await create_check(summa, user_id)
                                            error_message = (
                                                f"<b><blockquote>❌ {username}, вы забыли <u>дописать</u> <u>комментарий</u> к ставке.</blockquote></b>\n\n<i>Был совершён возврат денежных средств с комиссией 15%</i>"
                                            )
                                            await bot.send_message(config.CHANNEL_ID, error_message, reply_markup=create_keyboard(check, summa))
                                        else:
                                            error_message = (
                                                f"<b><blockquote>❌ {username}, вы забыли <u>дописать</u> <u>комментарий</u> к ставке.</blockquote></b>\n\n<i>Был совершён возврат денежных средств с комиссией 15%</i>\n<b>Заберите ваши деньги у</b> <i>администратора</i></blockquote></b>"
                                            )
                                            await bot.send_message(config.CHANNEL_ID, error_message,
                                                                   reply_markup=create_keyboard())
                                    else:
                                        count = 0

                                        for bet_type in DICE_CONFIG.keys():
                                            if bet_type == parsed_data['comment']:
                                                count += 1
                                                break

                                        if count == 0:
                                            cb_balance = get_cb_balance()
                                            summa = amount * (85 / 100)
                                            if float(cb_balance) >= float(summa) and float(summa) >= 0.02:
                                                check = await create_check(summa, user_id)
                                                await bot.send_message(config.CHANNEL_ID,
                                                                   f"<blockquote>❌ {parsed_data['name']}, <b>вы указали не верный комментарий к платежу!</b></blockquote>\n\n<b><i>Был совершён возврат денежных средств с комиссией 15%</i></b>", reply_markup=create_keyboard(check, summa))
                                            else:
                                                await bot.send_message(config.CHANNEL_ID,
                                                                       f"<blockquote><b>❌ {parsed_data['name']}, вы указали не верный комментарий к платежу!</b></blockquote>\n\n<i>Был совершён возврат денежных средств с комиссией 15%</i>\n\n<u>Заберите ваши деньги у</u> <i>администратора</i>",
                                                                       reply_markup=create_keyboard())
                                        else:
                                            bet_msg = await bet_sender.send_bet(username, amount, comment_lower)

                                            for bet_type in DICE_CONFIG.keys():
                                                if bet_type == parsed_data['comment']:
                                                    await handle_bet(parsed_data, bet_type, user_id, bet_msg, msg_id, processed_lines, line)
                                                    break
                                else:
                                    name = parsed_data['name']
                                    name = name.split("*")[0]
                                    await bot.send_message(config.CHANNEL_ID, f"<blockquote><b>❌ {name}, вы не включили пересылку сообщений!\n\nИнструкция по включения пересылки сообщений: <code>Настройки телеграмма ➙ Конфиденциальность ➙ Пересылка сообщений ➙ ( Кто может ссылаться на мой аккаунт при пересылке сообщений )</code>\n\nЗабрать ваши деньги можете у администратора.</b></blockquote>", reply_markup=create_keyboard())
                                processed_lines.append(line)
                                await asyncio.sleep(5)
                            with open(queue_file, 'w', encoding='utf-8') as file:
                                for line in lines:
                                    if line not in processed_lines:
                                        file.write(line)
                                return
                except Exception as e:
                    await bot.send_message(config.LOGS_ID, f"<blockquote><b>❌ Ошибка при обработке сообщения:</b><code>{str(e)}</code></blockquote>")
    except Exception as e:
        await bot.send_message(config.LOGS_ID, f"<blockquote><b>❌ Ошибка при обработке сообщения:</b><code>{str(e)}</code></blockquote>")

if __name__ == '__main__':
    with sqlite3.connect("db.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        us_id INT UNIQUE,
        join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        username TEXT,
        ref INT,
        ref_balance REAL DEFAULT 0.0,
        cashback REAL DEFAULT 0.0,
        ref_total REAL DEFAULT 0.0,
        msg_id INT
);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS deposits(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summa INT,
        us_id INT
);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS bets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summa REAL,
        win INT DEFAULT 0,
        lose INT DEFAULT 0,
        us_id INT
);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS settings(
        invoice_link TEXT PRIMARY KEY,
        max_amount DEFAULT 25,
        podkrut INT DEFAULT 0,
        stop INT DEFAULT 0
);""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS vemorr(
        id INT UNIQUE,
        payed INT DEFAULT 0,
        to_pay INT DEFAULT 0
);""")
        conn.commit()
        cursor.execute("INSERT OR IGNORE INTO vemorr(id,payed,to_pay) VALUES(1,0,0)")
        cursor.execute("INSERT OR IGNORE INTO settings(invoice_link) VALUES('https://google.com')")
        conn.commit()
    executor.start_polling(dp, skip_updates=True)
