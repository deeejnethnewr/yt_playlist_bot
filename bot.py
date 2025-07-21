import os
from pyrogram import Client, filters
from pytube import Playlist
from keep_alive import keep_alive

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("yt_playlist_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

keep_alive()

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Hello! Send me a YouTube playlist link to download all videos.")

@app.on_message(filters.text & filters.private)
async def download_playlist(client, message):
    url = message.text.strip()
    if "youtube.com/playlist" not in url:
        await message.reply("Please send a valid YouTube playlist link.")
        return

    await message.reply("Downloading playlist... please wait.")

    try:
        playlist = Playlist(url)
        for video in playlist.videos:
            file_path = video.streams.get_highest_resolution().download()
            await message.reply_video(file_path)
            os.remove(file_path)
    except Exception as e:
        await message.reply(f"Error: {e}")

app.run()
