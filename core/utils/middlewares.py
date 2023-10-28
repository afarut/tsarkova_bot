from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from core.models import TelgramUser
from asgiref.sync import sync_to_async


class UserRegisterMiddleware(BaseMiddleware):
    def __init__(self):
        super(UserRegisterMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        await sync_to_async(TelgramUser.objects.get_or_create)(
                telegram_id=message.chat.id, 
                username=message.chat.username, 
                name=f'{"" if message.chat.first_name else message.chat.first_name} {"" if message.chat.last_name else message.chat.last_name}'
            )

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        await self.on_process_message(call.message, data)