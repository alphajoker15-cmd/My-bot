# Placeholder for a Python bot

import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Your Telegram Bot Token ---
TOKEN = 8465552653:AAHbIVPzLmt1nLKdjGNNtKJcVPldHLDXIHI

# --- File size limits ---
TELEGRAM_FILE_LIMIT = 50 * 1024 * 1024  # 50 MB for free Telegram accounts
# TELEGRAM_FILE_LIMIT = 2 * 1024 * 1024 * 1024  # Uncomment for 2GB (Telegram Premium)

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a TikTok, Facebook, YouTube, X (Twitter), or Telegram Story link "
        "and I’ll download it for you!"
    )

# --- Download Video ---
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("⚠️ Please send a valid video link.")
        return

    await update.message.reply_text("⏳ Downloading your video... please wait.")

    try:
        # yt-dlp options
        ydl_opts = {
            "outtmpl": "video.%(ext)s",
            "format": "best[ext=mp4]/best",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Check file size
        file_size = os.path.getsize(filename)
        if file_size > TELEGRAM_FILE_LIMIT:
            size_mb = round(file_size / (1024 * 1024), 2)
            await update.message.reply_text(
                f"⚠️ The video is **{size_mb} MB**, which is larger than Telegram’s limit "
                f"({TELEGRAM_FILE_LIMIT // (1024*1024)} MB). I cannot send it."
            )
            os.remove(filename)
            return

        # Send the video
        await update.message.reply_video(video=open(filename, "rb"))

        # Clean up
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# --- Main ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()

if __name__ == "__main__":
    main()
