import time
from collections import deque, defaultdict
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Переменная BOT_TOKEN не найдена!")

user_messages = defaultdict(deque)

LIMIT = 7
TIME_WINDOW = 10
MENTION = "@Garsa555"

async def message_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()
    
    user_messages[user_id].append(now)

    while user_messages[user_id] and now - user_messages[user_id][0] > TIME_WINDOW:
        user_messages[user_id].popleft()

    if len(user_messages[user_id]) >= LIMIT:
        await update.effective_chat.send_message(MENTION)
        user_messages[user_id].clear()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, message_counter))
    print("Бот запущен...")
    app.run_polling()



