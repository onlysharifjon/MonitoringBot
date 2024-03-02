from aiogram.dispatcher import FSMContext

from bot import dp
from aiogram import types

from database import connect, cursor


@dp.message_handler(text="Xodimlar ro`yxati")
async def xodim_royxat(message: types.Message):
    malumotlar = cursor.execute("SELECT * FROM xodimlar").fetchall()
    txt = ""
    for i in malumotlar:
        txt += f"{i[0]})👨‍💻Xodim: <b>{i[3]}</b>\n\n🆔-> <code>{i[1]}</code>\n\n"
    await message.answer(txt)


from bot import Shogirdchalar


@dp.message_handler(text='Xodim qo`shish')
async def xodim_qoshish(message: types):
    await message.answer('Xodim ismini kiriting !')
    await Shogirdchalar.new_xodim_name.set()


@dp.message_handler(state=Shogirdchalar.new_xodim_name)
async def new_xodim_name(message: types.Message):
    global ismi
    ismi = message.text
    await message.answer('Xodim ID sini kiriting !')
    await Shogirdchalar.new_xodim_id.set()


@dp.message_handler(state=Shogirdchalar.new_xodim_id)
async def new_xodim_id(message: types.Message, state: FSMContext):
    id_user = message.text
    vaqt = message.date
    cursor.execute('INSERT INTO xodimlar(user_id, time, name) VALUES (?,?,?)', (id_user, vaqt, ismi))
    await message.answer(f'{ismi} Bazaga qo`shildi')
    await state.finish()
