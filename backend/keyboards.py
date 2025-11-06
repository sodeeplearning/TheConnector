from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


final_post_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выложить еще одно видео", callback_data="post")],
    [InlineKeyboardButton(text="Приступить к просмотру", callback_data="watch")]
])


categories_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=c, callback_data=c)]
        for c in config.categories
    ]
)
