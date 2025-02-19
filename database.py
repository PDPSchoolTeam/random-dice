import sqlite3
#
# # Connect to SQLite database
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
#
# # Define the users table if not exists
# cursor.execute(''' CREATE TABLE users (
# 			user_id VARCHAR(20) NOT NULL,
# 			full_name VARCHAR(200) NOT NULL,
# 			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
# 		);''')
#
# conn.commit()


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, full_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id,full_name) VALUES (?,?)", (user_id, full_name))

    def all(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, full_name FROM users").fetchall()

    def is_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))
