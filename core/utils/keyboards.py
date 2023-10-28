from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.models import Filter, TelegramUser
from asgiref.sync import sync_to_async


def start():
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


def menu(user_id):
	lst = []
	user = TelegramUser.objects.get(telegram_id=user_id)
	keyboard = InlineKeyboardMarkup()
	for ft in Filter.objects.all():
		if user.selected_filter == ft:
			lst.append(InlineKeyboardButton(f'✅{ft.name}', callback_data=f"set_filter:{ft.id}"))
		else:
			lst.append(InlineKeyboardButton(f'{ft.name}', callback_data=f"set_filter:{ft.id}"))
	keyboard.add(*lst)
	return keyboard 


async def async_menu(user_id):
	return await sync_to_async(menu)(user_id)