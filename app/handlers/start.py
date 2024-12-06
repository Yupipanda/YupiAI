from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from app.ai.aigentext import generate
from app.utils.allowed_users import ALLOWED_IDS


rt = Router()



@rt.message(CommandStart(), F.func(lambda msg: msg if msg.from_user.id in ALLOWED_IDS else None))
async def cmd_start(msg: Message):
    await msg.answer('Привет мой друг тататтатата')

