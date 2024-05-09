import os
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl

# Telegram Bot Token
TOKEN = '6910257402:AAGezJ_D-R3Wc8ur16XPb-vhpP0aDkWf89U'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the YouTube Playlist Downloader Bot! Send me the link to the YouTube playlist you want to download.")

# Function to download YouTube playlist and send MP3 files
def download_playlist(update, context):
    url = update.message.text

    # Options for youtube-dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }

    # Download the playlist
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        playlist_title = info_dict['title']

    # Get list of downloaded mp3 files
    mp3_files = [file for file in os.listdir() if file.endswith('.mp3')]

    # Send the mp3 files to the user
    for mp3_file in mp3_files:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(mp3_file, 'rb'), title=playlist_title)
        os.remove(mp3_file)  # Remove the downloaded mp3 file after sending

# Create Telegram bot handlers
def main():
    # Initialize Telegram bot
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers for commands
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Handler for messages containing YouTube playlist links
    dispatcher.add_handler(MessageHandler(Filters.regex(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/playlist'), download_playlist))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
