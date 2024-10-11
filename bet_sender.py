from pyrogram import Client, filters
import sqlite3
import asyncio

# Замените эти значения своими данными
api_id = "24355671"
api_hash = "6ed8a07c2178a9977a08aa7337520d60"
bot_token = "7970011168:AAFvBD9bWe5PgeBBB0rCqe1wm-Uar-TUFpQ"  # Замените на ваш токен бота
channel_id = "-1002293356681"  # Замените на ID вашего канала
crypto_bot_username = "YourCryptoBotUsername"  # Замените на имя вашего криптобота

app = Client("BetBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Функция для добавления ставки в базу данных
def add_bet_to_db(username, summa, bet_type):
    connection = sqlite3.connect('db.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO bets (username, summa, bet_type) VALUES (?, ?, ?)', (username, summa, bet_type))
    connection.commit()
    connection.close()

# Функция для отправки сообщения в канал
async def send_bet_message(username, summa, bet_type):
    message_text = (
        "*[⛈] Новая ставка!\n\n"
        f"> [👤] Никнейм игрока: {username}\n\n"
        f"> [💬] Игрок ставит на: {bet_type}\n\n"
        f"> [💰] Сумма ставки: {summa}$*"
    )
    await app.send_message(channel_id, message_text)

# Слушатель для комментариев к сообщениям
@app.on_message(filters.reply & filters.text)
async def handle_bet_comment(client, message):
    if message.reply_to_message.from_user.username == crypto_bot_username:
        try:
            parts = message.text.split()
            if len(parts) == 3:
                username = parts[0]
                summa = float(parts[1])
                bet_type = parts[2]
                
                # Добавляем ставку в базу данных
                add_bet_to_db(username, summa, bet_type)

                # Отправляем ставку в канал
                await send_bet_message(username, summa, bet_type)

                await message.reply("Ставка успешно добавлена и отправлена в канал!")
            else:
                await message.reply("Неверный формат. Используйте: username summa bet_type")
        except Exception as e:
            await message.reply(f"Ошибка: {e}")

if __name__ == "__main__":
    app.run()
