from db_connection.database_manager import DatabaseManager
from db_connection.db_sqlite_connector import DBSQLiteConnector


class QueryHandler:
    def __init__(self, use_sqlite=False, db_file=None):
        """
        use_sqlite=True => SQLite
        db_file        => если SQLite, то путь к файлу, например, 'database.db'
        """
        self.use_sqlite = use_sqlite
        # Создаём объект DatabaseManager, который сам выберет нужный коннектор
        self.db_manager = DatabaseManager(use_sqlite, db_file)
        # Автоматически создадим таблицу search_queries (с учётом search_count)
        self.create_search_queries_table()

    def create_search_queries_table(self):
        """
        Создаём таблицу search_queries, единообразную и для MySQL, и для SQLite:
          - id (PRIMARY KEY)
          - query_text
          - search_count
          - created_at
        """
        cursor = self.db_manager.get_cursor()

        if isinstance(self.db_manager.connector, DBSQLiteConnector):
            query = """
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT NOT NULL,
                search_count INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        else:
            query = """
            CREATE TABLE IF NOT EXISTS search_queries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query_text VARCHAR(255) NOT NULL,
                search_count INT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        cursor.execute(query)
        self.db_manager.commit()

    def save_search_query(self, query_text: str):
        """
        Если query_text уже есть в таблице - увеличим search_count
        Иначе вставим новую запись со search_count=1
        """
        cursor = self.db_manager.get_cursor()
        is_sqlite = isinstance(self.db_manager.connector, DBSQLiteConnector)

        if is_sqlite:
            # SQLite
            check_query = "SELECT search_count FROM search_queries WHERE query_text = ?"
            cursor.execute(check_query, (query_text,))
            row = cursor.fetchone()
            if row:  # Запись уже есть
                update_query = "UPDATE search_queries SET search_count = search_count + 1 WHERE query_text = ?"
                cursor.execute(update_query, (query_text,))
            else:
                insert_query = "INSERT INTO search_queries (query_text, search_count) VALUES (?, 1)"
                cursor.execute(insert_query, (query_text,))
        else:
            # MySQL
            check_query = "SELECT search_count FROM search_queries WHERE query_text = %s"
            cursor.execute(check_query, (query_text,))
            row = cursor.fetchone()
            if row:
                update_query = "UPDATE search_queries SET search_count = search_count + 1 WHERE query_text = %s"
                cursor.execute(update_query, (query_text,))
            else:
                insert_query = "INSERT INTO search_queries (query_text, search_count) VALUES (%s, 1)"
                cursor.execute(insert_query, (query_text,))

        self.db_manager.commit()

    def get_popular_searches(self, limit=5):
        """
        Возвращает популярные поисковые запросы (query_text, search_count), сортированные по убыванию.
        limit=5 => вернуть максимум 5 штук.
        """
        cursor = self.db_manager.get_cursor()
        is_sqlite = isinstance(self.db_manager.connector, DBSQLiteConnector)

        if is_sqlite:
            query = """
            SELECT query_text, search_count 
            FROM search_queries
            ORDER BY search_count DESC
            LIMIT ?
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
        else:
            query = """
            SELECT query_text, search_count 
            FROM search_queries
            ORDER BY search_count DESC
            LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()

        return rows

    # ---- Поиск фильмов ----
    # Предположим, что у вас в таблице film есть поля:
    # title, description, release_year и т.д.
    # Если структура таблицы другая — поправьте под себя.

    def search_movies_by_keyword(self, keyword):
        """
        Ищем фильмы, где description LIKE %keyword%
        (для примера) и сохраняем запрос в поисковую статистику.
        """
        # Сохраняем запрос
        self.save_search_query(keyword)

        cursor = self.db_manager.get_cursor()
        is_sqlite = isinstance(self.db_manager.connector, DBSQLiteConnector)

        if is_sqlite:
            sql = "SELECT * FROM film WHERE title like %s or description LIKE %s LIMIT 10"
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%",))
        else:
            sql = "SELECT * FROM film WHERE title like %s or description LIKE %s LIMIT 10"
            cursor.execute(sql, (f"%{keyword}%", f"%{keyword}%",))

        return cursor.fetchall()

    def search_movies_by_genre_and_year(self, genre, year):
        """
        Ищем фильмы по жанру и году.
        В демо-примере — связь через film_category + category (как в базе Sakila).
        """
        # Сохраняем запрос
        self.save_search_query(f"{genre} {year}")

        cursor = self.db_manager.get_cursor()
        is_sqlite = isinstance(self.db_manager.connector, DBSQLiteConnector)

        if is_sqlite:
            # SQLite-вариант
            sql = """
            SELECT a.title, a.release_year, a.description, c.name as genre
            FROM film AS a
            JOIN film_category AS b ON a.film_id = b.film_id
            JOIN category AS c ON b.category_id = c.category_id
            WHERE c.name = %s AND a.release_year = %s
            LIMIT 10
            """
            cursor.execute(sql, (genre, year))
        else:
            # MySQL-вариант (Sakila)
            sql = """
            SELECT a.title, a.release_year, a.description, c.name as genre
            FROM sakila.film AS a
            JOIN sakila.film_category AS b ON a.film_id = b.film_id
            JOIN sakila.category AS c ON b.category_id = c.category_id
            WHERE c.name = %s AND a.release_year = %s
            LIMIT 10
            """
            cursor.execute(sql, (genre, year))

        return cursor.fetchall()
