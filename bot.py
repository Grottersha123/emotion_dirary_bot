import asyncio
from collections import Counter
from contextlib import suppress

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN, TIME

from aiogram import Bot, types
import logging

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

emotion_list = ['радость 😀', 'удивление 😮', 'грусть 😔', 'гнев 🤬', 'отвращение 😕', 'презрение 🙄', 'страх 😱',
                'готово']
emotion_choosen = []
# button_time = InlineKeyboardButton('Time with people', callback_data='button2')
buttons = [InlineKeyboardButton(emotion_text, callback_data=f'button{index}')
           for index, emotion_text in enumerate(emotion_list[:-1])]
start_kb = InlineKeyboardMarkup(resize_keyboard=True)
start_kb.add(*buttons[:-2])
start_kb.add(buttons[-1], buttons[-2])
start_kb.add(InlineKeyboardButton(emotion_list[-1], callback_data=f'button{len(emotion_list) - 1}'))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

text_emotion = ''


# TODO:// написать обработчик start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Введите ваши мысли")


# TODO:// Написать обработчик help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("")


# TODO:// Написать обработчик кнопок
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global emotion_choosen
    code = callback_query.data[-1]
    code = int(code)
    if code == 7:
        emotion_temp = "\n".join('{} - {}'.format(v, k) for k, v in Counter(emotion_choosen[:]).items())
        emotion_choosen = []
        await bot.answer_callback_query(callback_query.id, text=f'ваше сообщение будет удалено через {TIME} сек')
        await bot.send_message(callback_query.from_user.id,
                               f"*{emotion_temp}* \n------------------\n**{text_emotion}**", parse_mode='markdown')
        asyncio.create_task(delete_message(callback_query.message, TIME))
    else:
        emotion_choosen.append(emotion_list[code])
        await bot.answer_callback_query(callback_query.id, text=f'Выбрали эмоцию {emotion_list[code]}')


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# TODO:// Реакции на ввод любого текста
@dp.message_handler()
async def any_text_message(message: types.Message):
    global text_emotion
    text_emotion = message.text
    logging.info(text_emotion)
    await message.reply('выберите эмоцию и шкалу какое у вас настроение', reply_markup=start_kb)
    asyncio.create_task(delete_message(message, TIME))


# TODO:// обработчик команды emotion

# TODO:// обработчик команды time

# TODO://  Написать запуск бота
if __name__ == '__main__':
    executor.start_polling(dp)
