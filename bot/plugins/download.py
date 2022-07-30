import os
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes
from bot.helpers.downloader import download_file
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError



@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video) & CustomFilters.auth_users)
def find_between( s, first_int, last ): #use first only int
    try:
        start = first_int #s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
def _telegram_file(client, message):
  user_id = message.from_user.id
  fname = message.text
  rname = message.caption
  print(rname)
  gname = find_between(rname,0,')')
  print(gname)
  sent_message = message.reply_text('🕵️**.ဖိုင်လင့်ကိုစစ်ဆေးနေပါသည်...**'+gname+').mp4', quote=True)
  if message.document:
    file = message.document
  elif message.video:
    file = message.video
  elif message.audio:
    file = message.audio
  sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.gname+').mp4', humanbytes(file.file_size), file.mime_type))
  LOGGER.info(f'Download:{user_id}: {file.file_id}')
  try:
    file_path = message.download(file_name=DOWNLOAD_DIRECTORY)
    sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
    msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
    sent_message.reply_text(msg)
  except RPCError:
    sent_message.edit(Messages.WENT_WRONG)
  LOGGER.info(f'Deleteing: {file_path}')
  os.remove(file_path)
