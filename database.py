import sqlite3

connect = sqlite3.connect('ishxonamonitoringi.db')
cursor = connect.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS xodimlar (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT NOT NULL, time TEXT)")
# XODIMLAR = [6132064182, 6380697731, 5699779185, 5318670320, 5321736122, 6666226459, 6108763026, 5919483106, 6983244704,
#             405326927,1010611866,5419954514,6015729113]
# NOMLARI = ["Muhammadaziz", "Abdulloh","Abduazim","Oqilxon","Farrux","Komiljon","Murodjon","Xayotilla", "Shamsiddin","Miraziz","Javohir","Islom","Abdulaziz"]
# for i in range(len(XODIMLAR)):
#     cursor.execute('INSERT INTO xodimlar(user_id, time, name) VALUES (?,?,?)', (XODIMLAR[i], '2024-03-02',NOMLARI[i]))
# connect.commit()
# cursor.execute('INSERT INTO xodimlar(user_id, time, name) VALUES (?,?,?)', (6216398846, '2024-03-02', "Zubayr"))
# connect.commit()


async def keldi_check(id_user, keldi_kun, oy, yil):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monitoring(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT,longitude TEXT,latitude TEXT,keldi TEXT NULL,keldi_kun INTEGER NULL,ketdi TEXT NULL,ketdi_kun INTEGER NULL,oy INTEGER,yil INTEGER)")
    connect.commit()
    check = cursor.execute("SELECT * FROM monitoring WHERE user_id=? AND keldi_kun=? AND oy=? AND yil=?",
                           (id_user, keldi_kun, oy, yil)).fetchone()
    return check


async def ketdi_check(id_user, ketdi_kun, oy, yil, *args, **partial_data):
    filtr_ketdi = cursor.execute("SELECT * FROM monitoring WHERE user_id=? AND ketdi_kun=? AND oy=? AND yil=?",
                                 (id_user, ketdi_kun, oy, yil)).fetchone()
    return filtr_ketdi


async def keldi_monitoring(user_id, longitude, latitude, keldi, keldi_kun, oy, yil):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monitoring(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT,longitude TEXT,latitude TEXT,keldi TEXT NULL,keldi_kun INTEGER NULL,ketdi TEXT NULL,ketdi_kun INTEGER NULL,oy INTEGER,yil INTEGER)")
    connect.commit()
    cursor.execute("INSERT INTO monitoring(user_id,longitude,latitude,keldi,keldi_kun,oy,yil) VALUES(?,?,?,?,?,?,?)",
                   (user_id, longitude, latitude, keldi, keldi_kun, oy, yil))
    connect.commit()


async def ketdi_monitoring(user_id, ketdi, keldi_kun, ketdi_kun):
    cursor.execute("UPDATE monitoring SET ketdi_kun=? , ketdi=? WHERE user_id=? AND keldi_kun=?",
                   (ketdi_kun, ketdi, user_id, keldi_kun))
    connect.commit()
    print('Sucsess')


async def xatolik(user_id, keldi_kun):
    cursor.execute("UPDATE monitoring SET user_id=?, keldi_kun='23:59:59' WHERE ketdi_kun=? AND ketdi=?",
                   (user_id, keldi_kun, keldi_kun))
    connect.commit()
#
