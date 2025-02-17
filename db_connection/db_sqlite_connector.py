import sqlite3

class DBSQLiteConnector:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.db_file)
            # Чтобы удобно получать столбцы по имени:
            self.connection.row_factory = sqlite3.Row
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
