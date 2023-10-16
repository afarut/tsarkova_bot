from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu():
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('🔍 Начать учить', callback_data=f"learn")) # strong
	return keyboard


def know_answer(question_id):
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('📖 Посмотреть ответ', callback_data=f"know_answer:{question_id}"))
	return keyboard


def mark_answer(question_id):
	keyboard = InlineKeyboardMarkup()
	keyboard.row(InlineKeyboardButton('5️⃣', callback_data=f"mark_answer:{question_id}:5"))
	keyboard.row(InlineKeyboardButton('4️⃣', callback_data=f"mark_answer:{question_id}:4"))
	keyboard.row(InlineKeyboardButton('3️⃣', callback_data=f"mark_answer:{question_id}:3"))
	keyboard.row(InlineKeyboardButton('2️⃣', callback_data=f"mark_answer:{question_id}:2"))
	return keyboard