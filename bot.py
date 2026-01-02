import os
from pyrogram import Client, filters
from config import *
from core.segmenter import split_video
from core.transform import transform_all
from core.merge import merge_all


app = Client(
"auto2sec",
api_id=API_ID,
api_hash=API_HASH,
bot_token=BOT_TOKEN
)


@app.on_message(filters.video)
async def handle_video(client, message):
os.makedirs(TEMP_DIR, exist_ok=True)
input_path = await message.download()


await message.reply("⏳ Editing started (2 sec per edit)...")


segments = split_video(input_path)
edited = transform_all(segments)
output = merge_all(edited)


await message.reply_video(output)


app.run()
