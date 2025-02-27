
import os
from idlelib.undo import Command

from aiogram.types import BotCommand
from dotenv import load_dotenv
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router

from query_handler import QueryHandler


load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
#storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

query_handler = QueryHandler(use_sqlite=True, db_file='/Users/svetlanapostel/PycharmProjects/FilmFinder/db.sqlite3')

@dp.message(BotCommand(command="start", description="test"))
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать! Используйте команды:\n"
                        "/search - поиск по ключевому слову\n"
                        "/search_by_genre_year - поиск по жанру и году\n"
                        "/popular_queries - популярные запросы")

@dp.message(['search'])
async def search_command(message: types.Message):
    # Предположим, что пользователь вводит ключевое слово после команды
    keyword = message.get_args()
    if not keyword:
        await message.reply("Пожалуйста, укажите ключевое слово для поиска.")
        return
    movies = query_handler.search_movies_by_keyword(keyword)
    if movies:
        response = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
    else:
        response = "Фильмы не найдены."
    await message.reply(response)

@dp.message(['search_by_genre_year'])
async def search_by_genre_year_command(message: types.Message):
    args = message.get_args().split(',')
    if len(args) != 2:
        await message.reply("Пожалуйста, укажите жанр и год в формате: жанр,год.")
        return
    genre, year = args
    movies = query_handler.search_movies_by_genre_and_year(genre.strip(), year.strip())
    if movies:
        response = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
    else:
        response = "Фильмы не найдены."
    await message.reply(response)

@dp.message(['popular_queries'])
async def popular_queries_command(message: types.Message):
    popular_queries = query_handler.get_popular_searches()
    if popular_queries:
        response = "\n".join([f"{query[0]} (поисков: {query[1]})" for query in popular_queries])
    else:
        response = "Нет популярных запросов."
    await message.reply(response)

if __name__ == '__main__':
    import asyncio

    # Запуск бота с помощью asyncio
    asyncio.run(dp.start_polling())