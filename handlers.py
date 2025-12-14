from telegram import Update
from telegram.ext import ContextTypes
from .config import *
from .processor import process_video


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send long video (15–20 min). Auto transform every 3 seconds."
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        video = update.message.video or update.message.document
        file = await context.bot.get_file(video.file_id)

        input_path = f"{DOWNLOAD_DIR}/{video.file_id}.mp4"
        output_path = f"{OUTPUT_DIR}/out_{video.file_id}.mp4"

        await file.download_to_drive(input_path)

        msg = await update.message.reply_text("Processing started… 0%")

        last_notified = 0

        def progress_callback(percent):
            nonlocal last_notified
            if percent >= 30 and last_notified < 30:
                context.application.create_task(
                    msg.edit_text("Processing… 30%")
                )
                last_notified = 30

            elif percent >= 60 and last_notified < 60:
                context.application.create_task(
                    msg.edit_text("Processing… 60%")
                )
                last_notified = 60

            elif percent >= 90 and last_notified < 90:
                context.application.create_task(
                    msg.edit_text("Processing… 90%")
                )
                last_notified = 90

        process_video(input_path, output_path, progress_callback)

        await msg.edit_text("Processing complete ✅ Uploading…")

        await update.message.reply_document(
            document=open(output_path, "rb")
        )

    except RuntimeError as e:
        await update.message.reply_text(
            f"❌ Error: {str(e)}\nTry shorter video or higher RAM server."
        )

    except Exception:
        await update.message.reply_text(
            "❌ Unexpected error occurred. Please try again later."
        )
