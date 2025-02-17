import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# Загрузим .env (убедитесь, что у вас есть .env с DB_HOST, DB_USER, DB_PASSWORD, DB_NAME и т.д.)
load_dotenv()

class DBConnector:
    def __init__(self):
        self.config = {
            'host': os.getenv("DB_HOST"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'database': os.getenv("DB_NAME"),
            'charset': os.getenv("DB_CHARSET", "utf8mb4"),
            'cursorclass': DictCursor
        }
        self.connection = None

    def connect(self):
        # Исправлено: проверяем self.connection, а не self.connect
        if not self.connection:
            self.connection = pymysql.connect(**self.config)
        return self.connection

    def get_cursor(self):
        if not self.connection:
            self.connect()
        return self.connection.cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
