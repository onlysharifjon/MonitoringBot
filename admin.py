from aiogram.dispatcher import FSMContext

from bot import dp, ADMINS
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
    if str(message.from_user.id) in ADMINS:
        await message.answer('Xodim ismini kiriting !')
        await Shogirdchalar.new_xodim_name.set()
    else:
        await message.answer('Siz admin emassiz')


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


@dp.message_handler(text='Xodimni o`chirish')
async def xodim_delete(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Xodim id ma`lumotini kiriting !')
        await Shogirdchalar.xodim_ochirish.set()
    else:
        await message.answer('Siz admin emassiz')


@dp.message_handler(state=Shogirdchalar.xodim_ochirish)
async def deleter(message: types.Message, state: FSMContext):
    xodim_id = message.text
    try:
        xodim_id = int(xodim_id)
        cursor.execute(f'DELETE FROM xodimlar WHERE user_id={xodim_id}')
        connect.commit()
        await message.answer('Xodim bazadan o`chirildi')
    except:
        await message.answer('Siz xato id kiritdingiz!😒')


@dp.message_handler(text="📝 1 kunlik ma`lumot")
async  def day_1(message:types.Message):
    day = str(message.date.day)
    month = str(message.date.month)
    year = str(message.date.year)

    check = cursor.execute("SELECT * FROM monitoring WHERE keldi_kun=? AND oy=? AND yil=?", (
        day, month, year)).fetchall()
    txt = ""
    txt+= f'⏳{year}-{month}-{day}\n\n'
    for i in check:
        txt+=f"Keldim: <i>{i[4]}</i> Ketdim: <i>{i[6]}</i>\n\n"
        print(i)
    await message.answer(txt)
