from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


final_post_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Приступить к просмотру", callback_data="watch")],
])

categories_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=c, callback_data=c)]
        for c in config.categories
    ]
)

short_video_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть полную версию видео", callback_data="full_video")],
        [InlineKeyboardButton(text="Задать вопрос ИИ", callback_data="ask_ai")],
        [InlineKeyboardButton(text="Сменить категорию видео", callback_data="watch")],
        [InlineKeyboardButton(text="Следующее видео", callback_data="next_video")],
    ]
)

long_video_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Задать вопрос ИИ", callback_data="ask_ai")],
        [InlineKeyboardButton(text="Сменить категорию видео", callback_data="watch")],
        [InlineKeyboardButton(text="Следующее видео", callback_data="next_video")],
    ]
)

ask_ai_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться к просмотру", callback_data="back")]
    ]
)
