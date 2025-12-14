import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, handle_video

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

print("🤖 Bot started successfully")
app.run_polling()
