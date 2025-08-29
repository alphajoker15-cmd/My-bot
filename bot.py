import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get your bot token from environment variable (Render → Environment)
TOKEN = os.getenv("8465552653:AAHbIVPzLmt1nLKdjGNNtKJcVPldHLDXIHI")

# Download function
def download_video(url: str, filename: str):
    ydl_opts = {
        "outtmpl": filename,
        "format": "bestvideo+bestaudio/best",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a video link (YouTube, TikTok, Facebook, X, etc.) and I'll download it for you!")

# Handle messages (links)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    filename = "video.mp4"
    try:
        await update.message.reply_text("📥 Downloading... please wait ⏳")

        download_video(url, filename)

        # Check file size before sending (Telegram limit ~50MB for normal bots)
        max_size = 49 * 1024 * 1024  # 49MB
        if os.path.getsize(filename) > max_size:
            await update.message.reply_text("⚠️ File is too large for Telegram (50MB limit). Try a shorter video.")
        else:
            await update.message.reply_video(video=open(filename, "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

# Run bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
