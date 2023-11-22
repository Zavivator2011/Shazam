import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import * 
from state import *
from utils import *


BOT_TOKEN = "6502882014:AAE31XBkaUL1HrUh4E1Wb7VwmbiGXDdLGQ8"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)



Admins = [1112362354,488486399]   

async def command_menu(dp: Dispatcher):
  await dp.bot.set_my_commands(
    [
      types.BotCommand('start', 'Ishga tushirish'),
    ]
  )
  await create_tables()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
  await add_user(message.from_user.id, message.from_user.username)
  await message.answer("Salom birodar")



@dp.message_handler(commands=['admin'])
async def admin_handler(message: types.Message):
    if message.from_user.id in Admins:
      users = await  get_all_users()
      await message.answer(f"Bot azolar soni: {users}")

      await AdminStates.mailing.set()





@dp.message_handler(commands=['send'])
async def send_handler(message: types.Message):
  if message.from_user.id in Admins:
    await message.answer("Xabarni yuboring:")

    await AdminStates.mailing.set()


@dp.message_handler(content_types=['text'], state=AdminStates.mailing)
async def mailing_state(message: types.Message,state: FSMContext):
  text = message.text
  context = message.content_type
  users = await get_all_id()
  
  await state.finish()

  for user in users:
    if context == 'text':
      await bot.send_message(chat_id=user[0], text=text)


@dp.message_handler(content_types=['video'])
async def get_user_video(message: types.Message):
    user_id = message.from_user.id
    filename = f"video_{user_id}.mp4"
    file_size = round(message.video.file_size / 1024 / 1024)
  
    if file_size <= 20:
        await message.video.download(destination_file=filename)

        result = await media_shazaming(filename)
        await message.reply(f"Nomi: {result[0]}\nIjrochi: {result[1]}")
        if len(result) == 3:
          await message.answer_audio(types.InputFile(result[-1]), caption="caption")
        
        await delete_user_media(user_id)
        
    else:
      await message.answer("20mb dan yuqori xajimdagi videoni tortaolmiman!")


if __name__ == "__main__":
  executor.start_polling(dp, on_startup=command_menu)