import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("API_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
XODIMLAR = env.list("XODIMLAR")  # xodimlar ro'yxati


class Shogirdchalar(StatesGroup):
    keldim = State()
    ketdim = State()


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


@dp.message_handler(text="📝 Ketdim", state="*")
async def ketdim(message: types.Message):
    await message.answer('Manzilingizni jo`nating!', reply_markup=location_button)
    await Shogirdchalar.ketdim.set()


@dp.message_handler(text="📝 Keldim", state="*")
async def keldim(message: types.Message):
    await message.answer('Manzilingizni jo`nating!', reply_markup=location_button)
    await Shogirdchalar.keldim.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=Shogirdchalar.ketdim)
async def locator_ketdim(message: types.Message):
    loc = message.location
    await bot.send_message(int(ADMINS[0]), f"{message.from_user.full_name} ishdan ketdi")
    await bot.send_location(int(ADMINS[0]), longitude=loc['longitude'], latitude=loc['latitude'])
    await message.answer('Manzilingiz Adminga Jo`natildi', reply_markup=xodim)


from database import keldi_monitoring, ketdi_monitoring, xatolik


@dp.message_handler(content_types=types.ContentType.LOCATION, state=Shogirdchalar.keldim)
async def locator_keldim(message: types.Message):
    loc = message.location

    await bot.send_message(int(ADMINS[0]), f"{message.from_user.full_name} ishga keldi")
    await bot.send_location(int(ADMINS[0]), longitude=loc.longitude, latitude=loc.latitude)
    await message.answer('Manzilingiz Adminga Jo`natildi', reply_markup=xodim)
    vaqt = str(message.date)
    list_vaqt = vaqt.split()
    await keldi_monitoring(message.from_user.id, str(loc.longitude), str(loc.latitude), list_vaqt[1],
                           message.date.day, message.date.month, message.date.year)


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def locator_ketdim(message: types.Message):
    vaqt = str(message.date)
    list_vaqt = vaqt.split()
    try:
        print(True)
        await ketdi_monitoring(message.from_user.id, list_vaqt[1], str(message.date.day), str(message.date.day))
        await message.answer('Xayr sog`bo`ling')
    except:
        print(False)
        await xatolik(message.from_user.id, message.date.day)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
