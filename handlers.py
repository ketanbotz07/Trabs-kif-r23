import os
from telegram import Update
from telegram.ext import ContextTypes
from .config import *
from .processor import process_video


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send long video. Auto transform every 3 seconds."
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.video.file_id)

    input_path = f"{DOWNLOAD_DIR}/{update.message.video.file_id}.mp4"
    output_path = f"{OUTPUT_DIR}/out_{update.message.video.file_id}.mp4"

    await file.download_to_drive(input_path)
    await update.message.reply_text("Processing… please wait")

    process_video(input_path, output_path)

    await update.message.reply_document(
        document=open(output_path, "rb")
    )
