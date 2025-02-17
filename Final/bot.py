import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from query_handler import QueryHandler

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Инициалинициализируем
query_handler = QueryHandler()

#/start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Привет! Я твой бот для поиска фильмов. Используй команды:\n"
        "/search - поиск по ключевому слову\n"
        "/search_by_genre_year - поиск по жанру и году\n"
        "/popular_queries - популярные запросы"
    )

# search по ключевому слову
def search(update: Update, context: CallbackContext) -> None:
    if context.args:
        keyword = " ".join(context.args)
        results = query_handler.search_movies_by_keyword(keyword)
        if results:
            message = "\n".join([f"Название: {movie['title']}, Год: {movie['year']}" for movie in results])
        else:
            message = "Фильмы по запросу не найдены."
        update.message.reply_text(message)
    else:
        update.message.reply_text("Пожалуйста, укажите ключевое слово для поиска.")

# search_by_genre_year по жанре и году
def search_by_genre_year(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 2:
        genre = context.args[0]
        year = context.args[1]
        results = query_handler.search_movies_by_genre_and_year(genre, year)
        if results:
            message = "\n".join([f"Название: {movie['title']}, Год: {movie['year']}" for movie in results])
        else:
            message = "Фильмы по жанру и году не найдены."
        update.message.reply_text(message)
    else:
        update.message.reply_text("Пожалуйста, укажите жанр и год (например, /search_by_genre_year Comedy 2022).")

# popular_queries
def popular_queries(update: Update, context: CallbackContext) -> None:
    results = query_handler.get_popular_searches()
    if results:
        message = "\n".join([f"Запрос: {result['query_text']}, Частота: {result['search_count']}" for result in results])
    else:
        message = "Популярные запросы не найдены."
    update.message.reply_text(message)

# запуск
def main() -> None:
    # Получаем токен, который был выдан BotFather
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

    # Созд-е объекта Updater
    updater = Updater(TELEGRAM_API_TOKEN)

    # Регистрируем обработчиков команд
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("search", search))
    updater.dispatcher.add_handler(CommandHandler("search_by_genre_year", search_by_genre_year))
    updater.dispatcher.add_handler(CommandHandler("popular_queries", popular_queries))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения работы
    updater.idle()

if __name__ == '__main__':
    main()

  # запуск python my_telegram_bot.py Перейдите в Telegram и найдите своего бота по username.
# Напишите команду /start, и бот должен ответить сообщением.

