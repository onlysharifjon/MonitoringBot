import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("API_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
XODIMLAR = env.list("XODIMLAR")  # xodimlar ro'yxati

from keyboards.default import admin, xodim, location_button

# ------------------------DATABASE--------------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def boshlovchi(message: types.Message):
    await message.answer('Assalomu Aleykum ' + message.from_user.first_name)
    print(ADMINS)
    if str(message.from_user.id) in ADMINS:
        await message.answer('Siz admin ekansiz', reply_markup=admin)
    elif str(message.from_user.id) in XODIMLAR:
        await message.answer('Siz Xodimsiz', reply_markup=xodim)
    else:
        await message.answer('Siz Bu botddan foydalanish huquqiga ega emassiz')


@dp.message_handler(text="📝 Ketdim")
async def ketdim(message: types.Message):
    await message.answer('Manzilingizni jo`nating!', reply_markup=location_button)


@dp.message_handler(text="📝 Keldim")
async def keldim(message: types.Message):
    await message.answer('Manzilingizni jo`nating!', reply_markup=location_button)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def locator(message: types.Message):
    loc = message.location
    await bot.send_message(int(ADMINS[0]), f"{message.from_user.full_name} ishga keldi")
    await bot.send_location(int(ADMINS[0]), longitude=loc['longitude'], latitude=loc['latitude'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
