import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '6115025348:AAHu9v0rujd0b_jSeBRc07nYMSeAkeLWKqU'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Питання та відповіді для міні-тесту
questions = [
    {
        "question": "Скільки планет у Сонячній системі?",
        "answers": ["7", "8", "9"],
        "correct_answer": 0
    },
    {
        "question": "Яка столиця Парижу?",
        "answers": ["Івано-Франківськ", "Лондон", "Париж"],
        "correct_answer":2
    },
    {
        "question":"PYTHON_1y_5_23 - 1 підгрупа топ?",
        "answers":['тта', "ньє"],
        "correct_answer":1
    }
]
user_data = {}
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item = KeyboardButton("Розпочати тест")
    markup.add(item)
    await message.answer("Привіт! Давай зробимо міні-тест. Натисни кнопку, щоб розпочати.", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Розпочати тест")
async def start_test(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {
        'current_question': 0,
        'score': 0
    }
    await show_question(user_id)


async def show_question(user_id):
    user = user_data[user_id]
    current_question = user['current_question']
    if current_question < len(questions):
        question_data = questions[current_question]
        question_text = question_data['question']
        answers = question_data['answers']

        random.shuffle(answers)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in answers:
            markup.add(KeyboardButton(answer))

        await bot.send_message(user_id, question_text, reply_markup=markup)

@dp.message_handler(lambda message: message.text in [answer for answer in sum((q['answers'] for q in questions), [])])
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    user = user_data[user_id]
    current_question = user['current_question']
    correct_answer = questions[current_question]['correct_answer']

    if message.text == questions[current_question]['answers'][correct_answer]:
        user['score'] += 1

    user['current_question'] += 1
    await show_question(user_id)

    user = user_data[user_id]
    current_question = user['current_question']
    
    if current_question < len(questions):
        pass
    else:
        score = user['score']
        await bot.send_message(user_id, f"Тест завершено! Твій результат: {score}/{len(questions)}")
        del user_data[user_id]


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)