import sqlite3

connect = sqlite3.connect('ishxonamonitoringi.db')
cursor = connect.cursor()


async def keldi_check(id_user, keldi_kun, oy, yil):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monitoring(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT,longitude TEXT,latitude TEXT,keldi TEXT NULL,keldi_kun INTEGER NULL,ketdi TEXT NULL,ketdi_kun INTEGER NULL,oy INTEGER,yil INTEGER)")
    connect.commit()
    check = cursor.execute("SELECT * FROM monitoring WHERE user_id=? AND keldi_kun=? AND oy=? AND yil=?", (id_user,keldi_kun,oy,yil)).fetchone()
    return check

async def ketdi_check(id_user, keldi_kun, oy, yil):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monitoring(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT,longitude TEXT,latitude TEXT,keldi TEXT NULL,keldi_kun INTEGER NULL,ketdi TEXT NULL,ketdi_kun INTEGER NULL,oy INTEGER,yil INTEGER)")
    connect.commit()
    check = cursor.execute("SELECT * FROM monitoring WHERE user_id=? AND keldi_kun=? AND oy=? AND yil=?", (id_user,keldi_kun,oy,yil)).fetchone()
    return check



























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
