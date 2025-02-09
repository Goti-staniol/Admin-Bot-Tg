import os

from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv


load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
group_router = Router()
private_router = Router()