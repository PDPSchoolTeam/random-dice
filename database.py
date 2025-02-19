import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        with self.connection:
            self.cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(20) NOT NULL PRIMARY KEY,
                    full_name VARCHAR(200) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                );
            ''')

    def add_user(self, user_id, full_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))

    def all(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, full_name FROM users").fetchall()

    def is_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT 1 FROM users WHERE user_id = ? LIMIT 1", (user_id,)).fetchone()
            return result is not None  # `fetchone()` natija bo'lsa `True`, aks holda `False`
