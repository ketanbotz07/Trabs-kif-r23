import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from video_processor import transform_video

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Send me a video (max 2 min).\n"
        "I will auto cut, zoom & transform it 🔥"
    )

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⏳ Processing video, please wait...")

    video = update.message.video or update.message.document
    file = await video.get_file()

    input_path = "input.mp4"
    output_path = "output.mp4"

    await file.download_to_drive(input_path)

    transform_video(input_path, output_path)

    await update.message.reply_video(
        video=open(output_path, "rb"),
        caption="✅ Video transformed (reuse-safe style)"
    )

    os.remove(input_path)
    os.remove(output_path)
    await msg.delete()

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
  
