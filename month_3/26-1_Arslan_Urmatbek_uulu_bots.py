from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import decouple
from decouple import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN=config('TOKEN')

bot = Bot(TOKEN)
db = Dispatcher(bot=bot)


@db.message_handler(commands=['start', 'hello'])

async def start_handler(massage:types.message):

    await massage.answer('HELLO!')
    await bot.send_message(massage.from_user.id,f'{massage.from_user.first_name}\nДля активации викторины---> /quiz')



@db.message_handler(commands=['quiz'])
async def quiz1(massage: types.Message):
    # создание кнопок
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton('next', callback_data='button')
    markup.add(button)

    ques = 'От куда этот мем?'
    answer = [
        'Из фильма "Терминатор"',
        'Из фильма "Человке-паук"',
        'Из фильма "Джокер"',
    ]
    photo = open('media/joker.jpg', 'rb')
    await bot.send_photo(massage.from_user.id, photo=photo)
    await bot.send_poll(
        chat_id=massage.from_user.id,
        question=ques,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        reply_markup=markup
    )

@db.callback_query_handler(text='button')
async def quiz2(call: types.CallbackQuery):
    ques = 'От куда этот мем?'
    answer = [
        'Из фильма "Мстители"',
        'Из рекламы казахского шампуня',
        'Из рекламы Old spice'
    ]
    photo = open('media/shampoo.jpg', 'rb')
    await bot.send_photo(call.from_user.id, photo=photo)
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=ques,
        options=answer,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        open_period=10

    )


@db.message_handler()
async def echo(massege:types.Message):
    await bot.send_message(massege.from_user.id,massege.text)


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(db, skip_updates=True)