from query_handler import QueryHandler

def show_popular_searches(qh: QueryHandler):
    popular = qh.get_popular_searches()
    for row in popular:
        print(f"{row['query_text']} - {row['search_count']} раз(а)")

def main():
    qh = QueryHandler(use_sqlite=False, db_file="database.db")

    while True:
        print("\n1. Поиск по ключевому слову")
        print("2. Поиск по жанру и году")
        print("3. Показать популярные запросы")
        print("4. Выход")

        choice = input("Введите номер действия: ").strip()
        if choice == "1":
            keyword = input("Введите ключевое слово для поиска: ")
            results = qh.search_movies_by_keyword(keyword)
            if results:
                for movie in results:
                    # movie — это sqlite3.Row или dict
                    title = movie["title"]
                    year = movie["release_year"]
                    print(f"Фильм: {title}, Год: {year}")
            else:
                print("Фильмы не найдены.")
        elif choice == "2":
            genre = input("Введите жанр: ")
            year = input("Введите год: ")
            results = qh.search_movies_by_genre_and_year(genre, year)
            if results:
                for movie in results:
                    print(f"Фильм: {movie['title']}, Год: {movie['release_year']}, Жанр: {movie['genre']}")
            else:
                print("Фильмы не найдены.")
        elif choice == "3":
            show_popular_searches(qh)
        elif choice == "4":
            print("Выход...")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    main()
