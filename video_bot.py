from telegram import Update, InputFile
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CONFIGURATION ===
BOT_TOKEN = "7670672591:AAE4E_Idcxj3NeF3ZwKQRzkHdLeN1f7GQPQ"  # Replace this before running
OWNER_ID = 1560194459  # Replace this with your Telegram user ID
VIP_CHANNEL_ID = -1002125275991  # Replace this with your VIP channel ID (not link)

# Caption to apply to every video
CUSTOM_CAPTION = '''
📲 <a href="https://t.me/PremiumCourse7765">Telegram Channel</a>
📱 <a href="https://whatsapp.com/channel/0029Vai3cmf2v1IvBuU6l21s">WhatsApp Channel</a>
🌐 <a href="https://www.paidcourse-infree.store/">Visit Our Website</a>

🔖 Contact: @Piyushyoutuber11
'''

# In-memory thumbnail path
THUMB_PATH = "user_thumb.jpg"

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized user.")
        return

    await update.message.reply_text(
        "👋 Welcome! Please send your video thumbnail image (JPG only)."
    )

# === THUMBNAIL HANDLER ===
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    await file.download_to_drive(THUMB_PATH)
    await update.message.reply_text("✅ Thumbnail saved. Now send your course videos.")

# === VIDEO HANDLER ===
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if not os.path.exists(THUMB_PATH):
        await update.message.reply_text("⚠️ Please send the thumbnail image first.")
        return

    message = await update.message.reply_text("🔄 Processing video...")

    video_file = await context.bot.get_file(update.message.video.file_id)
    video_path = "temp_video.mp4"
    await video_file.download_to_drive(video_path)

    # Send to VIP channel
    try:
        await context.bot.send_video(
            chat_id=VIP_CHANNEL_ID,
            video=open(video_path, 'rb'),
            caption=CUSTOM_CAPTION,
            thumb=InputFile(THUMB_PATH),
            parse_mode=ParseMode.HTML
        )
        await message.edit_text("✅ Video uploaded to VIP channel!")
    except Exception as e:
        await message.edit_text(f"❌ Upload failed: {e}")

    os.remove(video_path)

# === MAIN APP ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

print("Bot is running...")
app.run_polling()
