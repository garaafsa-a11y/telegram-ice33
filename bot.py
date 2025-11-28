import time
from collections import deque, defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8224209825:AAF5P8eNdnnx9c380oiMJhyv1KeHfVQETDE"

# Для каждого пользователя храним очередь сообщений
user_messages = defaultdict(deque)

LIMIT = 7          # сообщений
TIME_WINDOW = 10   # секунд
MENTION = "@Garsa555"

async def message_counter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = time.time()
    
    # Добавляем текущее время в очередь пользователя
    user_messages[user_id].append(now)

    # Удаляем старые сообщения
    while user_messages[user_id] and now - user_messages[user_id][0] > TIME_WINDOW:
        user_messages[user_id].popleft()

    # Проверяем лимит
    if len(user_messages[user_id]) >= LIMIT:
        await update.effective_chat.send_message(MENTION)
        user_messages[user_id].clear()

if name == "main":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, message_counter))
    print("Бот запущен...")
    app.run_polling()



