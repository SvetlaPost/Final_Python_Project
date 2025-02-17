
from db_connection.database_manager import DatabaseManager
from db_connection.db_sqlite_connector import DBSQLiteConnector

class QueryHandler:
    def __init__(self, use_sqlite=False, db_file="database.db"):
        """Создает обработчик запросов с возможностью работы с MySQL и SQLite."""
        self.db_manager = DatabaseManager(use_sqlite, db_file)

    def search_movies_by_keyword(self, keyword):
        """Ищу фильмы по ключевому слову"""
        cursor = self.db_manager.get_cursor()
        query = "SELECT * FROM film WHERE title LIKE ? OR description LIKE ? LIMIT 10" if isinstance(self.db_manager.connector, DBSQLiteConnector) else \
                "SELECT * FROM film WHERE title LIKE %s OR description LIKE %s LIMIT 10"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%",))
        results = cursor.fetchall()

        self.save_search_query(keyword)
        return results

    def search_movies_by_genre_and_year(self, genre, year):
        """Ищу фильмы по жанру и году"""
        cursor = self.db_manager.get_cursor()
        query = """
        SELECT title, description, release_year, c.name as genre
        FROM film AS a
        INNER JOIN film_category AS b ON a.film_id = b.film_id
        INNER JOIN category AS c ON b.category_id = c.category_id
        WHERE c.name = ? AND release_year = ? 
        LIMIT 10
        """ if isinstance(self.db_manager.connector, DBSQLiteConnector) else """
        SELECT title, description, release_year, c.name as genre
        FROM sakila.film AS a
        INNER JOIN sakila.film_category AS b ON a.film_id = b.film_id
        INNER JOIN sakila.category AS c ON b.category_id = c.category_id
        WHERE c.name = %s AND release_year = %s
        LIMIT 10
        """
        cursor.execute(query, (genre, year))
        results = cursor.fetchall()

        self.save_search_query(f"{genre}, {year}")
        return results

    def save_search_query(self, query_text):
        """Сохраняет поисковый запрос в таблицу"""
        cursor = self.db_manager.get_cursor()
        query = "INSERT INTO search_queries (query_text) VALUES (?)" if isinstance(self.db_manager.connector, DBSQLiteConnector) else \
                "INSERT INTO search_queries (query_text) VALUES (%s)"
        cursor.execute(query, (query_text,))
        self.db_manager.commit()

    def get_popular_searches(self):
        """Возвращает топ популярных поисковых запросов"""
        cursor = self.db_manager.get_cursor()
        query = "SELECT query_text, COUNT(*) as count FROM search_queries GROUP BY query_text ORDER BY count DESC LIMIT 5"
        cursor.execute(query)
        return cursor.fetchall()
