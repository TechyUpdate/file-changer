import os
import sys
import threading
import asyncio
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# --- 1. DUMMY WEB SERVER (RENDER KE LIYE) ---
web_app = Flask(__name__)
@web_app.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port, use_reloader=False)

threading.Thread(target=run_web, daemon=True).start()

# --- 2. ENVIRONMENT VARIABLES (STRICT CHECK) ---
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Yahan apna channel link daal dena 
CHANNEL_LINK = "https://t.me/DramaHub" 

# Agar Render me keys nahi daali, toh bot yahi chillayega aur band ho jayega
if not API_ID or not API_HASH or not BOT_TOKEN:
    print("\n❌ ERROR: API_ID, API_HASH ya BOT_TOKEN Render par theek se set nahi hai!\n")
    sys.exit(1) 

try:
    API_ID = int(API_ID)
except ValueError:
    print("\n❌ ERROR: API_ID sirf numbers me hona chahiye!\n")
    sys.exit(1)

# --- 3. ASYNCIO FIX (RENDER KE NAYE PYTHON VERSIONS KE LIYE) ---
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# --- 4. BOT INITIALIZATION ---
app = Client(
    "drama_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- 5. BOT LOGIC ---

# Bot check karne ke liye command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Haan bhai, main zinda hu! 🚀 Mujhe koi video ya file bhej.")

# Main video processing
@app.on_message(filters.video | filters.document)
async def process_video(client, message):
    # Bot silent na rahe, isliye pehle reply karega
    msg = await message.reply_text("⏳ Processing kar raha hu bhai...") 
    
    try:
        # Original caption lo ya default set karo
        caption = message.caption if message.caption else "New Episode"
        
        # Sirf pehli line (Title aur Quality) lo
        clean_title = caption.split('\n')[0]
        
        # Naya Caption Design (Tumhara watermark)
        new_caption = f"**{clean_title}**\n\n⚜️ Powered By : [ [Drama Hub] ]({CHANNEL_LINK})"
        
        # File ID extract karo
        file_id = message.video.file_id if message.video else message.document.file_id
        
        # Naye caption ke sath instantly forward karo
        await message.reply_video(
            video=file_id,
            caption=new_caption,
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Processing wala message hata do
        await msg.delete()
        
    except Exception as e:
        # Agar koi bhi error aaya, toh Telegram par bata dega
        await msg.edit_text(f"❌ Bhai error aa gaya:\n`{e}`")

# --- 6. START BOT ---
print("🚀 Bot is starting now...")
app.run()
