import os
import threading
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# --- Dummy Web Server for Render ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)

# Web server ko alag thread me start karna
threading.Thread(target=run_web, daemon=True).start()
# -----------------------------------

# Yahan Render environment variables se details aayengi
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client(
    "drama_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Tumhara custom link
CHANNEL_LINK = "https://t.me/your_channel_link"

@app.on_message(filters.video | filters.document)
async def update_video_caption(client, message):
    original_caption = message.caption if message.caption else "New Episode"
    title_line = original_caption.split('\n')[0] 
    
    new_caption = f"{title_line}\n\n⚜️ Powered By : [ [Drama Hub]({CHANNEL_LINK}) ]"
    
    file_id = message.video.file_id if message.video else message.document.file_id
    
    await message.reply_video(
        video=file_id,
        caption=new_caption,
        parse_mode=ParseMode.MARKDOWN
    )

print("Bot started...")
app.run()
