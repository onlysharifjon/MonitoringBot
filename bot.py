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
# XODIMLAR = env.list("XODIMLAR")  # xodimlar ro'yxati



class Shogirdchalar(StatesGroup):
    keldim = State()
    ketdim = State()
    new_xodim_name = State()
    new_xodim_id = State()
    xodim_ochirish = State()


from keyboards.default import admin, xodim, location_button
from database import connect,cursor
# ------------------------DATABASE--------------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands='start')
async def boshlovchi(message: types.Message):
    XODIMLAR_TEST = cursor.execute("SELECT user_id FROM xodimlar").fetchall()
    XODIMLAR = []
    for i in XODIMLAR_TEST:
        XODIMLAR.append(i[0])


    await message.answer('Assalomu Aleykum 👤' + message.from_user.first_name)

    if str(message.from_user.id) in ADMINS:
        await message.answer('👨🏻‍🔧 Siz admin ekansiz', reply_markup=admin)
    elif message.from_user.id in XODIMLAR:
        XODIMLAR = []
        await message.answer('👨🏻‍💻 Siz Xodimsiz', reply_markup=xodim)
    else:
        await message.answer('❌ Siz Bu botddan foydalanish huquqiga ega emassiz 🚷')


from database import keldi_check


@dp.message_handler(text="📝 Keldim", state="*")
async def keldim(message: types.Message):
    natija = await keldi_check(message.from_user.id, message.date.day, message.date.month, message.date.year)

    if natija is None:
        await message.answer('Manzilingizni jo`nating!', reply_markup=location_button)
        await Shogirdchalar.keldim.set()
    else:
        await message.answer('Siz Bugun ishga kelgansiz Yoqol')


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


from database import ketdi_check


@dp.message_handler(text="📝 Ketdim", state="*")
async def ketdim(message: types.Message):
    natija = await ketdi_check(message.from_user.id, message.date.day, message.date.month, message.date.year)
    if natija is None:
        await message.answer("Manzilingiznini Jo`nating",reply_markup=location_button)
        await Shogirdchalar.ketdim.set()
    else:
        await message.answer("Siz bugun Ishdan Ketgansiz")


from database import keldi_monitoring, ketdi_monitoring, xatolik


@dp.message_handler(content_types=types.ContentType.LOCATION, state=Shogirdchalar.ketdim)
async def locator_ketdim(message: types.Message):
    vaqt = str(message.date)
    list_vaqt = vaqt.split()
    try:

        await ketdi_monitoring(message.from_user.id, list_vaqt[1], str(message.date.day), str(message.date.day))
        await message.answer('Xayr sog`bo`ling')
    except:

        await xatolik(message.from_user.id, message.date.day)


if __name__ == '__main__':
    from admin import dp
    executor.start_polling(dp, skip_updates=True)
