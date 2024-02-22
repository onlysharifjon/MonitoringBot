import sqlite3

connect = sqlite3.connect('ishxona_monitoringi.db')
cursor = connect.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS monitoring(ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id BIGINT,longitude TEXT,latitude TEXT,keldi TEXT NULL,keldi_kun INTEGER NULL,ketdi TEXT NULL,ketdi_kun INTEGER NULL,oy INTEGER)")
connect.commit()


async def keldi_monitoring(user_id, longitude, latitude, keldi, keldi_kun, oy):
    cursor.execute("INSERT INTO monitoring(user_id,longitude,latitude,keldi,keldi_kun,oy) VALUES(?,?,?,?,?,?)",
                   (user_id, longitude, latitude, keldi, keldi_kun, oy))
    connect.commit()
