from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from core.models import TelegramUser
from asgiref.sync import sync_to_async


class UserRegisterMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserRegisterMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user = await sync_to_async(TelegramUser.objects.get_or_create)(telegram_id=message.chat.id)
        user = user[0]
        user.username=message.chat.username
        user.name=f'{"" if message.chat.first_name is None else message.chat.first_name} {"" if message.chat.last_name is None else message.chat.last_name}'
        await sync_to_async(user.save)()

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.on_process_message(call.message, data)