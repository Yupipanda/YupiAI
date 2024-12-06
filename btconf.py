from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message


LOGLEVEL = config('LOGLEVEL') # уровень логирования

REDIS_HOST = config('REDISHOST')

REDIS_PORT = config('REDISPORT')

REDIS_DB = config('REDISDB')

TOKEN = config('BOTTOKEN') # получение токена бота из .env файла

bot = Bot(token=TOKEN)





