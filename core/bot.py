from django.conf import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, types
import logging
from .models import Question, Answer
from asgiref.sync import sync_to_async
from .utils.keyboards import *
from datetime import datetime, timedelta
from .utils.middlewares import UserRegisterMiddleware


logging.basicConfig(filename="bot.log", level=logging.DEBUG)
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(UserRegisterMiddleware())


def question_serialize(q):
    question = {}
    question["id"] = q.id
    question["text"] = q.text
    question["answer"] = q.answer
    question["image"] = q.get_image()
    return question


def get_next_question(telegram_id):
    question = {}
    last = Answer.objects.filter(telegram_id=telegram_id).order_by("datetime").last()
    if last is None:
        return question_serialize(Question.objects.first())
    today = datetime.now()
    data = {i.id: 0 for i in Question.objects.all()}
    for i in Answer.objects.filter(datetime__day=today.day, datetime__year=today.year, telegram_id=telegram_id):
        data[i.question_id] += i.mark
    for i in Answer.objects.filter(datetime__day=today.day-1, datetime__year=today.year, telegram_id=telegram_id):
        data[i.question_id] += (i.mark // 2)
    for i in Answer.objects.filter(datetime__day=today.day-2, datetime__year=today.year, telegram_id=telegram_id):
        data[i.question_id] += (i.mark // 4)
    answers = sorted(list(zip(data.keys(), data.values())), key=lambda x: x[1])
    if answers[0][0] == last.question_id:
        return question_serialize(Question.objects.get(pk=answers[1][0]))
    return question_serialize(Question.objects.get(pk=answers[0][0]))


@dp.message_handler(commands=["start"], state="*")
async def bot_echo(message):
    await message.answer("Приветствую, этот бот поможет вам выучить большинство терминов и определений для сдачи Царьковой. \nС вопросами и предложениями пишите @afarut", reply_markup=start())


@dp.message_handler(commands=["menu"], state="*")
async def bot_echo(message):
    await message.answer("\"Я вам всё разжевала, осталось сделать только глотательный рефлекс\". Выберите фильтр:", reply_markup=menu())


@dp.callback_query_handler(lambda call: "learn" == call.data)
async def help(call):
    question = await sync_to_async(get_next_question)(call.message.chat.id)
    try:
        await call.message.delete()
    except Exception as e:
        logging.warning(e)
    if question['image'] is None:
        await call.message.answer(question["text"], reply_markup=know_answer(question["id"]))
    else:
        await call.message.answer_photo(question["image"], caption=question["text"], reply_markup=know_answer(question['id']))


@dp.callback_query_handler(lambda call: "know_answer" in call.data)
async def to_delivery_method(call, state):
    _, question_id = call.data.split(":")
    question = await sync_to_async(Question.objects.get)(pk=question_id)
    if not question.image:
        await call.message.edit_text(question.answer + "\n\nОцените на сколько вы были близки к ответу", reply_markup=mark_answer(question_id))
    else:
        await call.message.edit_caption(question.answer + "\n\nОцените на сколько вы были близки к ответу", reply_markup=mark_answer(question_id))


@dp.callback_query_handler(lambda call: "mark_answer" in call.data)
async def to_delivery_method(call, state):
    _, question_id, mark = call.data.split(":")
    await sync_to_async(Answer.objects.create)(telegram_id=call.message.chat.id, question_id=question_id, mark=int(2*int(mark)))
    await help(call)