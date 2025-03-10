import os
from dotenv import load_dotenv
from db_connection.db_connection import DBConnector       # Импортируем MySQL-коннектор
from db_connection.db_sqlite_connector import DBSQLiteConnector  # Импортируем SQLite-коннектор

# Если нужно, можно ещё раз подгрузить .env
load_dotenv()

class DatabaseManager:
    def __init__(self):
        """
        use_sqlite=True  => использовать SQLite
        use_sqlite=False => использовать MySQL (через DBConnector)
        db_file => путь к файлу SQLite (если нужно)
        """

        self.sakila_connector = DBConnector()
        self.sqlite_connector = DBSQLiteConnector("db.sqlite3")


    #def connect(self):
     #   return self.connector.connect()

    #def get_cursor(self):
     #   return self.connector.get_cursor()

    #def commit(self):
    #    self.connector.commit()

    #def rollback(self):
     #   self.connector.rollback()

    #def close(self):
     #   self.connector.close()

