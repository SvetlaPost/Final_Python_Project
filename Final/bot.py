
import os

from dotenv import load_dotenv
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from query_handler import QueryHandler


load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

query_handler = QueryHandler()

class SearchState(StatesGroup):
    waiting_for_keyword = State()
    waiting_for_genre_year = State()


@dp.message(Command(commands=["search"]))
async def search_command(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, укажите ключевое слово для поиска.")
    await state.set_state(SearchState.waiting_for_keyword)


@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.reply("Добро пожаловать в FilmFinder! Используйте команды:\n"
                        "/search - поиск по ключевому слову\n"
                        "/search_by_genre_year <жанр> <год> - поиск по жанру и году\n"
                        "/popular_queries - популярные запросы")


@dp.message(SearchState.waiting_for_keyword)
async def process_search_keyword(message: types.Message, state: FSMContext):
    keyword = message.text.strip()
    if not keyword:
        await message.reply("Ввели пустое сообщение, попробуйте снова")
        return

    movies = query_handler.search_movies_by_keyword(keyword)
    if movies:
        response = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
    else:
        response = "Фильмы не найдены."
    await message.reply(response)
    await state.clear()


@dp.message(Command(commands=["search_by_genre_year"]))
async def search_by_genre_year_command(message: types.Message, state: FSMContext):
    await message.reply("Пожалуйста, укажите жанр и год в формате: жанр год")
    await state.set_state(SearchState.waiting_for_genre_year)


@dp.message(SearchState.waiting_for_genre_year)
async def process_genre_year(message: types.Message, state: FSMContext):
    data = message.text.split()
    if len(data) != 2:
        await message.reply("Неправильный формат. Пожалуйста, укажите жанр и год в формате: жанр год")
        return

    genre, year = data[0], data[1]
    movies = query_handler.search_movies_by_genre_and_year(genre.strip(), year.strip())

    if movies:
        response = "\n".join([f"{movie['title']} ({movie['release_year']})" for movie in movies])
    else:
        response = "Фильмы не найдены."

    await message.reply(response)
    await state.clear()


@dp.message(Command(commands=["popular_queries"]))
async def popular_queries_command(message: types.Message):
    popular_queries = query_handler.get_popular_searches()
    if popular_queries:
        response = "Популярные запросы:\n" + "\n".join(
            [f"{query[0]} (поисков: {query[1]})" for query in popular_queries])
    else:
        response = "Нет популярных запросов."
    await message.reply(response)


if __name__ == "__main__":
    import asyncio

    # Запуск бота с помощью asyncio
    asyncio.run(dp.start_polling(bot))
