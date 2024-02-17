from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Oy ma`lumoti"),
            KeyboardButton(text="📝 7 kunlik ma`lumot"),
            KeyboardButton(text="📝 1 kunlik ma`lumot")
        ],
        [
            KeyboardButton(text="Xodim qo`shish"),
            KeyboardButton(text="Xodimlar ro`yxati"),
            KeyboardButton(text="Xodimni o`chirish")
        ]
    ],
    resize_keyboard=True
)

xodim = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Keldim"),

            KeyboardButton(text="📝 Ketdim"),
        ]
    ],
    resize_keyboard=True
)
location_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Joylashuv 🚩', request_location=True),
        ]
    ],
    resize_keyboard=True

)
